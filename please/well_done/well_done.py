import re
import os
import logging
from .. import log
from .. import globalconfig
from ..solution_tester import package_config
from ..utils.utests import get_tests
from ..utils.exceptions import PleaseException

OK, FIXED, CRASH = 0, 1, 2

logger = logging.getLogger("please_logger.well_done")

class WellDone:
    '''


    EXAMPLE: WellDone(['no_symbols_less_32', 
             'no_left_right_space', 'no_double_space', 'no_top_bottom_emptyline', 
             'endswith_EOLN', 'not_empty']).check('.tests/1')
    

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

    def __init__(self, check_functions_list):
        if check_functions_list is None:
            logger.warning("There is no validating functions for manual tests (see parameters well_done_tests and well_done_answers)")
            check_functions_list = []
        self.__check_functions_list = check_functions_list

    def check_functions_list(self):
        return self.__check_functions_list

    def endswith_EOLN(self):
        if len(self.__content) == 0 or self.__content[-1] != '\n':
            self.__content += '\n'
            logger.warning("FIXED : There was no \"\\n\" in the end of file %s", self.__path, exc_info = 0)
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
        if result == FIXED:
            logger.warning("FIXED : There were excess spaces in line beginnings in file %s", self.__path, exc_info = 0)
        return result

    def no_right_space(self):
        result = OK
        if re.search(r'\ $', self.__content):
            result = FIXED
            self.__content = re.sub(r'\ +$', '', self.__content)
        if re.search(r'\ \n', self.__content):
            result = FIXED
            self.__content = re.sub(r'\ *\n', '\n', self.__content)
        if result == FIXED:
            logger.warning("FIXED : There were excess spaces in line ends in file %s", self.__path, exc_info = 0)        
        return result

    def no_left_right_space(self):
        return max(self.no_left_space(), self.no_right_space())

    def no_symbols_less_32(self):
        for c in self.__content:
            code = ord(c)
            if ord(c) < 32 and c != '\n':
                logger.error("There are symbols with code less, than 32 in file %s", self.__path, exc_info = 0) 
                return CRASH
        return OK

    def no_double_space(self):
        if re.search(r'\ \ ', self.__content):
            self.__content = re.sub(r'\ \ +', r' ', self.__content)
            logger.warning("FIXED : There were double spaces in file %s", self.__path, exc_info = 0)
            return FIXED
        else:
            return OK
     
    def no_top_emptyline(self):
        result = OK
        lines_list = self.__content.split("\n")
        if len(lines_list) == 2 and lines_list[1] == "":
            return result
        if re.search(r'^\n', self.__content):
            result = FIXED
            self.__content = re.sub(r'^\n+', '', self.__content)
            logger.warning("FIXED : There was an empty line in top of file %s", self.__path, exc_info = 0)            
        return result

    def no_bottom_emptyline(self):
        result = OK
        lines_list = self.__content.split("\n")
        if len(lines_list) == 2 and lines_list[1] == "":
            return result
        if re.search(r'\n\n$', self.__content):
            result = FIXED
            self.__content = re.sub(r'\n\n+$', '\n', self.__content)
            logger.warning("FIXED : There was an empty line in bottom of file %s", self.__path, exc_info = 0)
        return result

    def no_top_bottom_emptyline(self):
        return max(self.no_top_emptyline(), self.no_bottom_emptyline())

    def not_empty(self):
        #check if file contains __non-space__ characters
        if re.search(r'\S',self.__content) is None:
            logger.error("There is no content in %s", self.__path, exc_info = 0)
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
        if result == FIXED:
            logger.warning("FIXED : There was an empty line in file %s", self.__path, exc_info = 0)
        return result

    def __rewrite(self):
        #write down modified content of file
        with open(self.__path, 'w', encoding = "utf-8") as f:
            f.write(self.__content)

    def check(self, path, fix_inplace=True):
        with open(path, encoding = 'utf-8') as file:
            self.__content = file.read()
        self.__path = path
        self.__fixes = []
        #apply each checking function to the content of the file
        for function_name in self.__check_functions_list:
            #to operate with splitted list with unknown spaces
            function_name = function_name.strip()
            #TODO: potentially dangerous
            try:
                result = getattr(self, function_name)()
            except AttributeError:
                print(self.__check_functions_list)
                raise PleaseException("There is no validating function " + function_name + 
                                       ", check default.package properties (well_done_test, well_done_answer)")
            if result == CRASH:
                return (CRASH, [function_name])
            elif result == FIXED:
                self.__fixes += [function_name]
        if self.__fixes:
            if fix_inplace:
                self.__rewrite()
            return (FIXED, self.__fixes)
        else:
            return (OK, [])
