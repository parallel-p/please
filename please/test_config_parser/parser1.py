import string
import os
from ..language.language import Language
from .. import globalconfig

class TestInfo:
    """
    TestInfo contains information about single line of configuration file
    that contains information about single test or test generator or command.
    TestInfo __init__ takes 2 arguments: number of current line in configuration
    file and current line.
    The information is:
    * line - current line of configuration file
    * line_number - number of current line in configuration file
    * attributes - dictionary, contains attributes of current line.
      These attributes are situated in square brackets and divided by comma.
      Single attribute can be a tag (corresponded in attributes as <tag> = None)
      or an equal (<key> = <value>, corresponded in attributes as <key> = <value>)
    * type - TestInfoType information about current line
    * command - contains:
      - file name if type is FILE
      - tuple (<command>, <list of arguments>) if type is COMMAND
      - tuple (<generator name>, <list of arguments>) if type is GENERATOR
    * attributes_str - current line attributes
    * operator - line without arguments
    * whitespace_prefix - maximal prefix of current line, contains only 
      whitespace symbols (it will be useful for do python-style attributes)
    
    Example:
    
        test_info = TestInfo(32, "    [sample, scope=10, DP = 1] generator.cpp 1 2 3")
        
        test_info.attributes == { 'sample' : None, 'scope' : 10, 'DP' : '1' }    
        test_info.operator == ' generator.cpp 1 2 3'
        test_info.type == TestInfoType.GENERATOR
        test_info.command == ('generator.cpp', ['1', '2', '3'])
        test_info.whitespace_prefix == '    '
        test_info.attributes_str == 'sample,  scope=10, DP = 1'
        
    """
    
    def __init__(self, line_number=None, line=None):
        if not (line is None and line_number is None):
            self.line_number = line_number
            self.line = line
            
            self.whitespace_prefix = self.__get_whitespace_prefix(line)
    
            self.__line = line.strip()
            self.attributes = self.__get_attributes_and_make_operator()
    
            tokens = [token for token in self.operator.split(' ') if token != '']
            #tokens = non-empty words from self.operator
            
            if tokens == []:
                raise EnvironmentError("tests config parser: Line %d: no operator" % (self.line_number))
            
            tokens[0] = self.__do_normal_path(tokens[0])
            first_token = tokens[0]
            
            if self.__is_command(first_token):
                self.type = TestInfoType.COMMAND
                self.command = self.__tokens_to_command(tokens)
            elif self.__is_generator(first_token):
                self.type = TestInfoType.GENERATOR
                self.command = self.__tokens_to_command(tokens)
            elif len(tokens) != 1: #if it is not command either generator, it must be
                                   #single filename
                raise EnvironmentError("tests config parser: Line %d: expected 1 argument, more found" % (self.line_number))
            elif self.__is_file(first_token):
                self.type = TestInfoType.FILE
                self.command = self.__to_file(first_token)
            else:
                raise EnvironmentError("tests config parser: Line %d cannot be parsed (maybe there is no such file?)" % (self.line_number))
            
    def __do_normal_path(self, path):
        result = ''
        for token in path.split('/'):
            for subtoken in token.split('\\'):
                result = os.path.join(result, subtoken)
        return result
        
    def __get_whitespace_prefix(self, line):
        first_not_whitespace = 0
        while first_not_whitespace < len(line) and line[first_not_whitespace] in string.whitespace:
            first_not_whitespace += 1
        return line[0 : first_not_whitespace]
    
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
        
    def __tokens_to_command(self, tokens):
        #first token is a name of command or probram, follows are arguments
        return (tokens[0], tokens[1 : len(tokens)])
        
    def __get_attributes_and_make_operator(self):
        """
        Gets attributes from a line (if they are provided)        
        '[sample, scope = 10 , DP] test01' => { 'sample' : None, 'scope' : 10, 'DP' : None }
        Make self.operator
        '[sample, scope = 10 , DP] testgen.dpr 3 4 5' => self.operator == ' testgen.dpr 3 4 5'
        """
        
        result = {}
        self.attributes_str = ''
        
        if self.__line == "" or self.__line[0] != '[':
            self.operator = self.__line
            return result #self.__line (corresponds self.line.strip()) is an empty
                          #line or doesn't contain attributes
        
        if self.__line.find(']') == -1:
            raise EnvironmentError("tests config parser: Line %d: wrong format, ']' expected" % (self.line_number))
                                   
        self.attributes_str = self.__line[1 : self.__line.find(']')]
        attributes_list = self.attributes_str.split(',')
        
        for attribute in attributes_list:
            if attribute.find('=') > -1: #if attribute is '<key> = <value>'
                key_and_value = attribute.split('=')
                key = key_and_value[0].strip()
                value = key_and_value[1].strip()
            else:                        #attribute is a single tag
                key = attribute.strip()
                value = None
            result[key] = value
            
        self.operator = self.__line.replace('['+self.attributes_str+']', "")
        #delete attributes from self.line.strip()
            
        return result  
    
    def __command_to_tokens(self, command):
        return [command[0]] + command[1]
    
    def constructor(self, attributes, type, command, whitespace_prefix='', line_number=0):
        self.whitespace_prefix = whitespace_prefix
        self.attributes = attributes
        self.type = type
        self.command = command
        attributes_list=[]
        for key, value in self.attributes.items():
            if (value == None):
                new_item = str(key)
            else:
                new_item = str(key)+' = '+str(value)
            attributes_list.append(new_item)
        self.attributes_str = ', '.join(attributes_list)
        self.line_number = line_number
        if self.type == TestInfoType.FILE:
            self.operator = command
        else:
            self.operator = ' '.join(self.__command_to_tokens(command))
        self.line = self.whitespace_prefix+'['+self.attributes_str+'] '+self.operator
    
    def __str__(self):
        return self.line

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
            new_test = TestInfo(line_number + 1, line)
            result.append(new_test)
            
        return result

class TestInfoType:
    """
    contains a type of current line
    """
    FILE =  "file"
    COMMAND = "command"
    GENERATOR = "generator"
