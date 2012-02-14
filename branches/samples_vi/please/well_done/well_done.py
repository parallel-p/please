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

EOLN = ord('\n')
LINESEP = os.linesep.encode()

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
    
    def _msg_FIXED(self, msg):
        logger.warning("FIXED : %s %s", msg, self.__path)
        return FIXED # for convenience

    def endswith_EOLN(self):
        if not self.__content.endswith(b'\n'):
            self.__content += b'\n'
            return self._msg_FIXED("There was no end of line in the end of file")
        else:
            return OK

    def __regexp_based_fix(self, regexp, repl, message):
        self.__content, repls = regexp.subn(repl, self.__content)
        if repls:
            return self._msg_FIXED(message)
        return OK

    _left_space_re = re.compile(b'^\\ +', re.MULTILINE)

    def no_left_space(self):
        return self.__regexp_based_fix(self._left_space_re, b'',
                                       "There were excess spaces in line beginnings in file")

    _right_space_re = re.compile(b'\\ +$', re.MULTILINE)

    def no_right_space(self):
        return self.__regexp_based_fix(self._right_space_re, b'',
                                       "There were excess spaces in line ends in file")

    def no_left_right_space(self):
        return max(self.no_left_space(), self.no_right_space())

    def no_symbols_less_32(self):
        for code in self.__content:
            if code < 32 and code != EOLN:
                logger.error("There are symbols with code less than 32 in file %s", self.__path, exc_info = 0) 
                return CRASH
        return OK

    _multispace_re = re.compile(b'\\ {2,}')

    def no_double_space(self):
        return self.__regexp_based_fix(self._multispace_re, b' ',
                                       "There were double spaces in file")
     
    def no_top_emptyline(self):
        if self.__content.startswith(b'\n'):
            # One empty line case
            if len(self.__content) == 1:
                return OK
            self.__content = self.__content.lstrip(b'\n')
            return self._msg_FIXED("There was an empty line in top of file")
        return OK

    def no_bottom_emptyline(self):
        if self.__content.endswith(b'\n\n'):
            self.__content = self.__content.rstrip(b'\n') + b'\n'
            return self._msg_FIXED("There was an empty line in bottom of file")
        return OK

    def no_top_bottom_emptyline(self):
        return max(self.no_top_emptyline(), self.no_bottom_emptyline())

    def not_empty(self):
        #check if file contains __non-space__ characters
        if not self.__content.strip():
            logger.error("There is no content in %s", self.__path, exc_info = 0)
            return CRASH
        return OK
    
    _emptyline_re = re.compile(b'\n{2,}') # I wish that could be written as b'^$', but
                                          # some strange issue in re prevents it.

    def no_emptyline(self):
        msg = "There was an empty line in file"
        result = self.__regexp_based_fix(self._emptyline_re, b'\n', msg)
        if self.__content.startswith(b'\n'):
            self.__content = self.__content.lstrip(b'\n')
            return self._msg_FIXED(msg)
        return result

    def __rewrite(self):
        #write down modified content of file
        with open(self.__path, 'wb', newline = None) as f:
            f.write(self.__content.replace(b'\n', LINESEP))

    _universal_newline_re = re.compile(b'\r(?!\n)|\r\n|\n')

    def check(self, path, fix_inplace=True):
        with open(path, 'rb') as file:
            content = file.read()
            self.__content = self._universal_newline_re.sub(b'\n', content)
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
