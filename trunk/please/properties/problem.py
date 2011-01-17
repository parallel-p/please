import checker
import statements
import validator 

import os.path

#TODO: move parsing to separate class?
class Problem:
    def __init__(self, file_system, filename = "problem.properties"):
        if not file_system.exists(filename):
            raise Exception("No '%s' file" % filename)

        import configparser
        from io import StringIO
        parser = configparser.ConfigParser()
        section = "default"
        parser.readfp(
            StringIO(
                "[%s]\n" % section +
                str(file_system.read(filename))
            )
        )

        self.__validator = self.__construct_validator(parser)
        self.__checker = self.__construct_checker(parser)
        self.__statements = self.__construct_statements(parser)
        self.__input = self.__get(parser, "input", "stdin")#TODO: is it ok to use default here?
        self.__output = self.__get(parser, "output", "stdout")#TODO: is it ok to use default here?

    def __construct_validator(self, parser):
        #TODO: how about solution as validator?
        file = self.__get(parser, "validator")
        if file != None:
            return validator.Validator(file)
        else:
            return None
            
    def __construct_checker(self, parser):
        #TODO: how about standard checker?
        file = self.__get(parser, "check")#TODO: or checker?
        if file != None:
            return checker.Checker(file = file)
        else:
            return None

    def __construct_statements(self, parser):
        file = self.__get(parser, "statements")
        #TODO: is it ok to force statements to be in directory statements?
        if file != None:
            file = os.path.join("statements", file)#TODO: some config or just here?
            #TODO: I am hate repeating like "statements.Statements" too.
            #How to do this better? Just import class on top of file?
            return statements.Statements(file)
        else:
            return None

    def validator(self):
        return self.__validator    

    def checker(self):
        return self.__checker

    def statements(self):
        return self.__statements

    #TODO: add main solution properties

    def input(self):
        return self.__input

    def output(self):
        return self.__output

    def __get(self, parser, param, default = None):
        args = ("default", param)
        if parser.has_option(*args):
            return parser.get(*args)
        else:
            return default

if __name__ == "__main__":
    cfg_context = \
"""
please_version=0.1
tags=naive

input=aplusb.in
output=aplusb.out

check=check.cpp
validator=val.pas
"""
    from mock import Mock
    read_mock = Mock(return_value = cfg_context)
    exists_mock = Mock(return_value = True)
    fs = Mock()
    fs.read = read_mock
    fs.exists = exists_mock

    problem = Problem(fs)
    assert(problem.input() == "aplusb.in")
    assert(problem.output() == "aplusb.out")
    
    validator = problem.validator()
    #TODO: mock this class. just check constructor called
    assert(validator.file() == "val.pas")
    assert(validator.input() == "stdin")
    assert(validator.output() == "stdout")

    checker = problem.checker()
    #TODO: mock this class. just check constructor called
    assert(checker.file() == "check.cpp")

    statements = problem.statements()
    #TODO: mock this class. just check constructor called
    assert(statements == None)

