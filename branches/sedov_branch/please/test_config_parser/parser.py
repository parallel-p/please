import os
import re
import glob
from .. import language
from please import globalconfig
from ..test_info import file_test_info, cmd_gen_test_info, echo_test_info, python_test_info
from ..utils.exceptions import PleaseException

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
        check = language.get(token)
        return check is not None and check != 'command'
    
class TestObjectFactory:    
    @staticmethod
    def create(well_done, line_number, first_token, others=[], attr={}, comment = ''):
        def add_eoln_modificator(str):
            if not str.endswith("\n"):
                str += "\n"
            return str

        if TokenSpecificator.is_echo(first_token):
            return echo_test_info.EchoTestInfo(' '.join(others), attr, comment)
        elif TokenSpecificator.is_python(first_token):
            modificator = None
            if well_done and "endswith_EOLN" in well_done.check_functions_list():
                modificator = add_eoln_modificator
            return python_test_info.PythonTestInfo(' '.join(others), modificator, attr, comment)
        elif TokenSpecificator.is_generator(first_token):
            return cmd_gen_test_info.CmdOrGenTestInfo(first_token, others, attr, comment)
        elif len(others) > 0: 
            raise PleaseException("Tests config parser: Line %d: expected 1 argument, more found" % (line_number))
        elif TokenSpecificator.is_file(first_token):
            return file_test_info.FileTestInfo(first_token, attr, well_done, comment)
        else:
            raise PleaseException("Tests config parser: Line %d cannot be parsed (maybe there is no such file?)" % (line_number))
        
class TestConfigParser:
    def __init__(self, config, well_done=None):
        self.__parsed = []
        self.__test_config = config
        self.__well_done = well_done
        for line_number, line in enumerate(self.__test_config.split('\n')):
            if (line.strip() == ''):  #empty line
                continue
            parsed_line = self.__parse_line(line_number + 1, line.strip())
            if parsed_line is not None: 
                self.__parsed.append(parsed_line)
    
    def get_binaries(self):
        result = []
        for item in self.__parsed:
            if(TokenSpecificator.is_generator(item[1]) and item[1] not in result):
                result.append(item[1])
        return result
    
    def count_by_tag(self, tag):
        amount = 0
        for line in self.__parsed:
            if tag in line[3]:
                amount += 1
        return amount
    
    def get_test_info_objects(self):       
        result = []
        for item in self.__parsed:
            result.append(TestObjectFactory.create(self.__well_done, *item))
        return result
   
    def __find_closed_bracket(self, line):
        balans = 0
        for idx, c in enumerate(line):
            if c == "[": balans += 1
            if c == "]":
                balans -= 1
                if balans == 0:
                    return idx
        return -1

    def __parse_line(self, line_number, line):
        """
        takes line number & stripped line
        returns list like [line_number, first_token, [other_tokens], {attributes}, comment] or None, if it's an empty line
        """
        attribs = {}
        if line[0] == '[':
            closed_bracket = self.__find_closed_bracket(line)
            if closed_bracket == -1:
                raise PleaseException("Tests config parser: Line %d: wrong format, ']' expected" % (line_number))
                                   
            attributes_str = line[1 : closed_bracket]
            attributes_list = attributes_str.split(',')
        
            for attribute in attributes_list:
                if '=' in attribute: #if attribute is '<key> = <value>'
                    key_and_value = attribute.split('=')
                    key = key_and_value[0].strip()
                    value = key_and_value[1].strip()
                else:                        #attribute is a single tag
                    key = attribute.strip()
                    value = None
                attribs[key] = value
            new_line = line[closed_bracket + 1 : ]
        else:
            new_line = line
        comment = ''
        if new_line.rfind('#') > -1:
            new_line, comment = new_line.rsplit('#', 1)
        new_line.strip()
        tokens = new_line.split()
        if tokens == []:
            return None
        tokens[0] = self.__do_normal_path(tokens[0])
        return [line_number, tokens[0], tokens[1 : len(tokens)], attribs, comment]
    
    def __do_normal_path(self, path):
        result = [item for item in re.split("\\\\|/", path) if item != ''] #split by / and \\
        return os.path.join(*result)
   
class FileTestConfigParser(TestConfigParser):
    def __init__(self, well_done = None, path = globalconfig.default_tests_config):
        if not os.path.exists(path):
            raise PleaseException("There is no tests configuration file ({0})!".format(path))
        with open(path) as config_file:
            super(FileTestConfigParser, self).__init__(config_file.read(), well_done)

