import re
import os
import logging
from .. import log
from .. import globalconfig
from ..solution_tester import package_config
from ..test_config_parser import parser2
from ..utils.utests import get_tests

OK, FIXED, CRASH = 0, 1, 2

logger = logging.getLogger("please_logger.well_done")

class WellDone:
    '''
    USAGE:   WellDone(path_to_file, list_of_funcnames).check()


    EXAMPLE: WellDone('.tests/1', ['no_symbols_less_32', 
             'no_left_right_space', 'no_double_space', 'no_top_bottom_emptyline', 
             'endswith_EOLN', 'not_empty']).check()
    

    Checks and if possible - repair the file according to the rules.

    Returns pair (result, list_of_function_names)
    
    If result == OK, then list_of function_names == []
    
    If result == FIXED, it consist of all functions, that return FIXED,
    and the file is changed according this rules.
    
    If result == CRASHED, list consist of the name of one function - which found
    inconsistency but can't change file (for example, file is empty).

    Please, check tests BEFORE validate, 
    answers - immediately after they are generated.
    '''

    def __init__(self, path, check_functions_list):
        self.__path = path
        self.__check_functions_list = check_functions_list
        with open(path, encoding = "utf-8") as f:
            self.__content = f.read()

###################################################################
# Check functions block
###################################################################

    def endswith_EOLN(self):
        if len(self.__content) == 0 or self.__content[-1] != '\n':
            self.__content += '\n' 
            return FIXED
        else:
            return OK

    def no_left_space(self):
        result = OK
        if re.search(r'^\ ', self.__content):
            result = FIXED
            self.__content = re.sub(r'^\ +', '', self.__content)
        if re.search(r'\n\ ', self.__content):
            result = FIXED
            self.__content = re.sub(r'\n\ *', '\n', self.__content)
        return result

    def no_right_space(self):
        result = OK
        if re.search(r'\ $', self.__content):
            result = FIXED
            self.__content = re.sub(r'\ +$', '', self.__content)
        if re.search(r'\ \n', self.__content):
            result = FIXED
            self.__content = re.sub(r'\ *\n', '\n', self.__content)
        return result

    def no_left_right_space(self):
        return max(self.no_left_space(), self.no_right_space())

    def no_symbols_less_32(self):
        for c in self.__content:
            code = ord(c)
            if ord(c) < 32 and c != '\n':
                return CRASH
        return OK

    def no_double_space(self):
        if re.search(r'\ \ ', self.__content):
            self.__content = re.sub(r'\ \ +', r' ', self.__content)
            return FIXED
        else:
            return OK
     
    def no_top_emptyline(self):
        result = OK
        if re.search(r'^\n', self.__content):
            result = FIXED
            self.__content = re.sub(r'^\n+', '', self.__content)
        return result

    def no_bottom_emptyline(self):
        result = OK
        if re.search(r'\n\n$', self.__content):
            result = FIXED
            self.__content = re.sub(r'\n\n+$', '\n', self.__content)
        return result

    def no_top_bottom_emptyline(self):
        return max(self.no_top_emptyline(), self.no_bottom_emptyline())

    def not_empty(self):
        #check if file contains __non-space__ characters
        if re.search(r'\S',self.__content) is None:
            return CRASH
        else:
            return OK

    def no_emptyline(self):
        result = OK
        if re.search(r'^\n', self.__content):
            result = FIXED
            self.__content = re.sub(r'^\n+', '', self.__content)
        if re.search(r'\n\n', self.__content):
            result = FIXED
            self.__content = re.sub(r'\n\n+', '\n', self.__content)
        return result

###################################################################
# End of check functions block
###################################################################

    def __rewrite(self):
        #write down modified content of file
        with open(self.__path, 'w', encoding = "utf-8") as f:
            f.write(self.__content)

    def check(self):
        #apply each checking function to the content of the file
        self.__fixes = []
        for function_name in self.__check_functions_list:
            #dirty trick to operate with splitted lists with unknown spaces
            function_name = function_name.strip()
            
            result = getattr(self, function_name)()
            if result == CRASH:
                return (CRASH, [function_name])
            elif result == FIXED:
                self.__fixes += [function_name]
        if self.__fixes:
            self.__rewrite()
            return (FIXED, self.__fixes)
        else:
            return (OK, [])

class WellDoneCheck:
    '''Check that all tests are WellDone
       USAGE: result = WellDoneCheck.all() #result is bool
    
    '''


    def __init__(self):
        
        #need to rebuild tests
        self.rebuild = False
        
        #need to fix and rebuild tests
        self.fix_and_rebuild = False

        self.config = package_config.PackageConfig.get_config('.')
        if self.config:
            if 'well_done_test' in self.config and self.config['well_done_test'] not in ["", None]:
                self.well_done_test = list(map(str.strip, self.config["well_done_test"].split(',')))
            else:
                logger.warning("Well_done config for tests is empty")
            if 'well_done_answer' in self.config and self.config['well_done_answer'] not in ["", None]:
                self.well_done_answer = list(map(str.strip, self.config["well_done_answer"].split(',')))
            else:
                logger.warning("Well_done config for answers is empty")
         #   self.tests_info = parser2.parse_test_config()


    def __test(self, filename, function_list, log_text = ''):
        #check test or answer file and write result to the log
        #in future this function must return verdict to be analysed by test generator
        result = WellDone(os.path.join(filename), function_list).check()

        if log_text:
            log_prefix = log_text + ' '
        else:
            log_prefix = os.path.basename(filename) + ' ' 

        if result[0] == OK:
            logger.info(log_prefix + 'well-done')
        elif result[0] == FIXED:
            logger.warning(log_prefix + 'fixed with ' + ', '.join(result[1]))
            self.rebuild = True
        else:
            logger.error(log_prefix + 'crashed while checking ' + result[1][0])
            self.fix_and_rebuild = True

    def __tests(self):
        self.rebuild = False
        self.fix_and_rebuild = False

        logger.info('\n\nChecking generated tests')
        for test in self.tests_info:
            #do not check manual tests again
            if test.type != TestInfoType.FILE:
                log_text = globalconfig.default_tests_config + ':line ' + str(test.line_number) + ':test:' + " ".join([test.command[0], " ".join(test.command[1])]) + ':'
                self.__test(os.path.join('.tests', str(test.line_number)), self.well_done_test, log_text)
        if self.fix_and_rebuild:
            logger.error('Please fix generators or commands in tests config and generate all tests again.')
            return False
        elif self.rebuild:
            logger.error('Generated tests were fixed. But you should fix generators or tests config and generate all tests again.')
            return False
        else:
            return True

    def __answers(self):
        self.rebuild = False
        self.fix_and_rebuild = False

        logger.info('\n\nChecking tests\' answers')
        for test in self.tests_info:
            if test.type != TestInfoType.FILE:
                log_text = globalconfig.default_tests_config + ':line ' + str(test.line_number) + ':answer:' + " ".join([test.command[0], " ".join(test.command[1])]) + ':'
            else:
                log_text = globalconfig.default_tests_config + ':line ' + str(test.line_number) + ':answer:' + str(test.command) + ':'
            self.__test(os.path.join('.tests', str(test.line_number)) + '.a', self.well_done_answer, log_text)
        if self.fix_and_rebuild:
            logger.error('Please fix main solution generate all answers again.')
            return False
        elif self.rebuild:
            logger.error('Generated answers were fixed. But you should fix main solution and generate all tests again.')
            return False
        else:
            return True

    def __sources(self):
        #check all manual tests' sources
        logger.info('\n\nChecking manual tests source files')
        for test in self.tests_info:
            if test.type == TestInfoType.FILE:
                log_text = globalconfig.default_tests_config + ':line ' + str(test.line_number) + ':manual test:' + test.command + ':'
                self.__test(test.command, self.well_done_test, log_text)
        if self.fix_and_rebuild:
            logger.error('Please fix manual tests and generate all tests again.')
            return False
        elif self.rebuild:
            logger.error('Manual tests were fixed. Please, generate all tests again.')
            return False
        else:
            return True


    def all(self):
        '''check manual test sources, then generated tests, then generated answers
           returns True if all are well done, and False otherwise
        '''
        if not self.__sources():
            return False
        elif not self.__tests():
            return False
        elif not self.__answers():
            return False
        else:
            logger.info('All tests and answers are well done')
            return True    