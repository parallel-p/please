import os
import re
import glob
from ..language.language import Language
from please import globalconfig
from ..test_info import file_test_info, cmd_gen_test_info, echo_test_info, python_test_info

class TokenSpecificator:    
    @staticmethod
    def is_echo(token):
        return token == 'echo'
    
    @staticmethod
    def is_python(token):
        return token == 'python'
    
    @staticmethod
    def is_file(token):
        #if file exists, it is a file
        return glob.glob(token) != []
    
    @staticmethod
    def is_generator(token):
        #if we can determine the programming language of file token, it is generator
        lang = Language()
        check = lang.get(token)
        return check is not None and check != 'command'
    
class TestObjectFactory:    
    @staticmethod
    def create(well_done, line_number, first_token, others=[], attr={}, comment = ''):
        if TokenSpecificator.is_echo(first_token):
            return echo_test_info.EchoTestInfo(' '.join(others), attr, comment)
        elif TokenSpecificator.is_python(first_token):
            return python_test_info.PythonTestInfo(' '.join(others), attr, comment)
        elif TokenSpecificator.is_generator(first_token):
            return cmd_gen_test_info.CmdOrGenTestInfo(first_token, others, attr, comment)
        elif len(others) > 0: 
            raise EnvironmentError("Tests config parser: Line %d: expected 1 argument, more found" % (line_number))
        elif TokenSpecificator.is_file(first_token):
            return file_test_info.FileTestInfo(first_token, attr, well_done, comment)
        else:
            raise EnvironmentError("Tests config parser: Line %d cannot be parsed (maybe there is no such file?)" % (line_number))
        
class TestConfigParser:
    def __init__(self, config, well_done=None):
        self.__parsed = []
        self.__test_config = config
        self.__well_done = well_done
        for line_number, line in enumerate(self.__test_config.split('\n')):
            if (line.strip() == ''):  #empty line
                continue
            self.__parsed.append(self.__parse_line(line_number + 1, line.strip()))
    
    def get_binaries(self):
        result = []
        for item in self.__parsed:
            if(TokenSpecificator.is_generator(item[1]) and item[1] not in result):
                result.append(item[1])
        return result
    
    def get_test_info_objects(self):       
        result = []
        for item in self.__parsed:
            result.append(TestObjectFactory.create(self.__well_done, *item))
        return result
    
    def __parse_line(self, line_number, line):
        """
        takes line number & stripped line
        returns list like [line_number, first_token, [other_tokens], {attributes}, comment]
        """
        attribs = {}
        if line[0] == '[':
            if line.find(']') == -1:
                raise EnvironmentError("Tests config parser: Line %d: wrong format, ']' expected" % (line_number))
                                   
            attributes_str = line[1 : line.find(']')]
            attributes_list = attributes_str.split(',')
        
            for attribute in attributes_list:
                if attribute.find('=') > -1: #if attribute is '<key> = <value>'
                    key_and_value = attribute.split('=')
                    key = key_and_value[0].strip()
                    value = key_and_value[1].strip()
                else:                        #attribute is a single tag
                    key = attribute.strip()
                    value = None
                attribs[key] = value
            new_line = line[line.find(']') + 1 : ]
        else:
            new_line = line
        comment = ''
        if new_line.rfind('#') > -1:
            new_line, comment = new_line.rsplit('#', 1)
        new_line.strip()
        tokens = new_line.split()
        if tokens == []:
            raise EnvironmentError("Tests config parser: Line %d: no operator" % (line_number))
        tokens[0] = self.__do_normal_path(tokens[0])
        return [line_number, tokens[0], tokens[1 : len(tokens)], attribs, comment]
    
    def __do_normal_path(self, path):
        result = [item for item in re.split("\\\\|/", path) if item != ''] #split by / and \\
        return os.path.join(*result)
   
class FileTestConfigParser(TestConfigParser):
    def __init__(self, well_done = None, path = globalconfig.default_tests_config):
        with open(path) as config_file:
            super(FileTestConfigParser, self).__init__(config_file.read(), well_done)

