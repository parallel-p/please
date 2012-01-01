import string
import os
from please.language.language import Language
from please import globalconfig
from please.test_info import file_test_info
from please.test_info import cmd_gen_test_info

class TestObjectFactory:
    def __init__(self, line_number, line):
        self.__line = line.strip()
        self.__line_number = line_number
    
    def create(self):
        self.__attributes = self.__get_attributes_and_make_operator()
        
        tokens = [token for token in self.__operator.split(' ') if token != '']
        #tokens = non-empty words from self.__operator
                
        if tokens == []:
            raise EnvironmentError("Tests config parser: Line %d: no operator" % (self.__line_number))
        
        first_token = self.__do_normal_path(tokens[0])
        if self.__is_command(first_token) or self.__is_generator(first_token):
            return cmd_gen_test_info.CmdOrGenTestInfo(first_token, tokens[1 : len(tokens)], self.__attributes)
        elif len(tokens) != 1: 
            raise EnvironmentError("Tests config parser: Line %d: expected 1 argument, more found" % (self.__line_number))
        elif self.__is_file(first_token):
            return file_test_info.FileTestInfo(self.__to_file(first_token), self.__attributes)
        else:
            raise EnvironmentError("Tests config parser: Line %d cannot be parsed (maybe there is no such file?)" % (self.__line_number))
                
    def __do_normal_path(self, path):
        result = ''
        for token in path.split('/'):
            for subtoken in token.split('\\'):
                result = os.path.join(result, subtoken)
        return result
    
    def __is_command(self, token):
        #command echo is the only supported command now
        #list will contain more elements in future
        return token in ['echo'] 
    
    def __to_file(self, token):
        return os.path.join(".", token)
    
    def __is_file(self, token):
        #if file exists, it is a file
        return os.path.exists(self.__to_file(token))
            
    def __is_generator(self, token):
        #if we can determine the programming language of file token, it is generator
        lang = Language()
        check = lang.get(token)
        return check is not None and check != 'command'
    
    def __get_attributes_and_make_operator(self):
        """
        Gets attributes from a line (if they are provided)        
        '[sample, scope = 10 , DP] test01' => { 'sample' : None, 'scope' : 10, 'DP' : None }
        Make self.__operator
        '[sample, scope = 10 , DP] testgen.dpr 3 4 5' => self.__operator == ' testgen.dpr 3 4 5'
        """
        
        result = {}
        attributes_str = ''
        
        if self.__line == "" or self.__line[0] != '[':
            self.__operator = self.__line
            return result #self.__line (corresponds self.__line.strip()) is an empty
                          #line or doesn't contain attributes
        
        if self.__line.find(']') == -1:
            raise EnvironmentError("tests config parser: Line %d: wrong format, ']' expected" % (self.__line_number))
                                   
        attributes_str = self.__line[1 : self.__line.find(']')]
        attributes_list = attributes_str.split(',')
        
        for attribute in attributes_list:
            if attribute.find('=') > -1: #if attribute is '<key> = <value>'
                key_and_value = attribute.split('=')
                key = key_and_value[0].strip()
                value = key_and_value[1].strip()
            else:                        #attribute is a single tag
                key = attribute.strip()
                value = None
            result[key] = value
            
        self.__operator = self.__line.replace('[' + attributes_str+']', "")       
        #deletes attributes from self.__line.strip()
            
        return result
    
def parse_test_config():
    """
    Parse configuration file 'tests.please', returns list 
    of TestInfo for each non-empty line. If single line is
    uncorrect, raises exception.
    
    Example:
      list_of_tests = parse_test_config()
    """
    with open(globalconfig.default_tests_config, 'r', encoding='utf-8') as test_config_file:
        result = []
        
        test_config = test_config_file.read()
        
        for line_number, line in enumerate(test_config.split('\n')):
            if (line.strip() == ''):  #empty line
                continue
            new_test = TestObjectFactory(line_number+1, line).create()
            result.append(new_test)
            
        return result