#/bin/python3
import os
import logging
from ..utils.exceptions import PleaseException

#"" is for commands
langs = ["c", "c++", "c#", "pascal", "delphi", "python2", "python3", "java", ""]

class Language:
    '''
    This class determines in which programming language given
    source code file is written.
    Currently it's very stupid, so don't mix extensions and
    don't be sad if it has made a mistake.

    Example:
    Language lang()
    print(lang().get("test_files/helloworld.pas")) # outputs pascal
    print(lang().get("test_files/helloworld3.py")) # outputs python3
    '''
    def __init__(self):
        pass

    def __by_ext(self, fn):
        ext = os.path.splitext(fn)[1].lower()
        if not ext:
            return 'command'
        dct = { ".c" : "c",
                ".cc" : "c++",
                ".cpp" : "c++",
                ".c++" : "c++",
                ".cs" : "c#",
                ".pas" : "pascal",
                ".java" : "java",
                ".py" : "?python",
                ".dpr" : "delphi",
                ".tex" : "latex"
                 }
        if (ext in dct):
            return dct[ext]
        else:
            return None

    def __proceed_python(self, path):
        with open(path, 'r') as f:
            line = f.readline()
        if (line.find("python3") != -1):
            return "python3"
        elif (line.find("python2") != -1):
            return "python2"
        else:
            log = logging.getLogger("please_logger.language")
            log.warning("Assuming " + path + " is python2 file. \nIf you want to translate it with python3, insert 'python3' in the comment in the first line of this file")
            return "python2"

    def __by_contents(self, path, info):
        if (info[1:] == "python"):
            return self.__proceed_python(path)
        else:
            return None

    def get(self, path):
        """Returns None if no language supported"""
        res_by_ext = self.__by_ext(path)
        if (res_by_ext is None):
            return None
        if (res_by_ext[0] != '?'):
            return res_by_ext
        if (not os.path.isfile(path)):
            raise PleaseException("There is no file " + path)
        res_by_content = self.__by_contents(path, res_by_ext)
        return res_by_content

def is_source_code(path):
    detector = Language()
    lang = detector.get(path)
    return lang is not None and lang != "command"

