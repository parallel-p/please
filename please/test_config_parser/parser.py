import os
import re
from ..language.language import Language
from please import globalconfig
from ..test_info import file_test_info
from ..test_info import cmd_gen_test_info

class TokenSpecificator:
    @staticmethod
    def is_command(token):
        #command echo is the only supported command now
        #list will contain more elements in future
        return token in ['echo'] 
    
    @staticmethod
    def is_file(token):
        #if file exists, it is a file
        return os.path.exists(TokenSpecificator.convert_path(token))
    
    @staticmethod
    def convert_path(token):
        return os.path.join(".", token)
    
    @staticmethod
    def is_generator(token):
        #if we can determine the programming language of file token, it is generator
        lang = Language()
        check = lang.get(token)
        return check is not None and check != 'command'
    
class TestObjectFactory:    
    @staticmethod
    def create(line_number, first_token, others=[], attr={}):
        if TokenSpecificator.is_command(first_token) or TokenSpecificator.is_generator(first_token):
            return cmd_gen_test_info.CmdOrGenTestInfo(first_token, others, attr)
        elif len(others) > 0: 
            raise EnvironmentError("Tests config parser: Line %d: expected 1 argument, more found" % (line_number))
        elif TokenSpecificator.is_file(first_token):
            return file_test_info.FileTestInfo(TokenSpecificator.convert_path(first_token), attr)
        else:
            raise EnvironmentError("Tests config parser: Line %d cannot be parsed (maybe there is no such file?)" % (line_number))
        
class TestConfigParser:
    def __init__(self, config):
        self.__parsed = []
        self.__test_config = config
        for line_number, line in enumerate(self.__test_config.split('\n')):
            if (line.strip() == ''):  #empty line
                continue
            self.__parsed.append(self.__parse_line(line_number + 1, line))
    
    def get_binaries(self):
        result = []
        for item in self.__parsed:
            if(TokenSpecificator.is_generator(item[1]) and item[1] not in result):
                result.append(item[1])
        return result
    
    def get_test_info_objects(self):       
        result = []
        for item in self.__parsed:
            result.append(TestObjectFactory.create(*item))
        return result
    
    def __parse_line(self, line_number, line):
        """
        takes line number & stripped line
        returns list like [line_number, first_token, [other_tokens], {attributes}]
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
        string_without_attr = line[line.find(']') + 1 : ]
        tokens = string_without_attr.split() #all items are stripped
        if tokens == []:
            raise EnvironmentError("Tests config parser: Line %d: no operator" % (line_number))
        tokens[0] = self.__do_normal_path(tokens[0])
        return [line_number, tokens[0], tokens[1 : len(tokens)], attribs] 
    
    def __do_normal_path(self, path):
       result = [item for item in re.split("\\\\|/", path) if item != ''] #split by / and \\
       return os.path.join(*result)
   
class FileTestConfigParser(TestConfigParser):
    def __init__(self, path = globalconfig.default_tests_config):
        with open(path) as config_file:
            super(FileTestConfigParser, self).__init__(config_file.read())