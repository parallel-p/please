import re
import os
import logging
from .. import log
from .. import globalconfig

OK, FIXED, CRASH = 0, 1, 2

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


def well_done_check_test(filename, function_list):
    #check test or answer file and write result to the log
    #in future this function must return verdict to be analysed by test generator
    logger = logging.getLogger("please_logger.well_done")
    result = WellDone(os.path.join(filename), function_list).check()
    if result[0] == OK:
        logger.info(filename + ' is well-done')
    elif result[0] == FIXED:
        logger.info(filename + ' was fixed with ' + ', '.join(result[1]))
    else:
        logger.info(filename + ' check was crashed while testing with ' + result[1][0])

