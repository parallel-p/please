#/bin/python3
import os
import logging
import re
import mimetypes

from ..utils.exceptions import PleaseException

#"" is for commands
langs = ["c", "c++", "c#", "pascal", "delphi", "python2", "python3", "java", ""]


# Trying to access libmagic.
# libmagic is a library distributed with file(1) and commonly found on
# Linux distributions; it guesses type or MIME-type of file with searching
# of certain byte sequences within it.

try:
    from . import magic
except (OSError, ImportError):
    magic = None

MAPPINGS = { # mappings for some MIME synonyms
    'x-csrc': 'x-c',
    'x-chdr': 'x-c',
    'x-c++src': 'x-c++',
    'x-c++hdr': 'x-c++',
}

KNOWN_MIMES = { # all MIMES that we are interested in
    'x-c': 'c', 
    'x-c++': 'c++',
    'x-csharp': 'c#',
    'x-pascal': 'pascal',
    'x-delphi': 'delphi',
    'x-python': '?python',
    'x-java': 'java',
    'x-tex': 'latex',
    'x-empty': None,
}

logger = logging.getLogger("please_logger.language")

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
    FALLBACK_MIMETYPES = os.path.join(os.path.dirname(__file__), 'mime.types')

    def __init__(self):
        self.mimedb = mimetypes.MimeTypes()
        if os.path.isfile(self.FALLBACK_MIMETYPES):
            self.mimedb.read(self.FALLBACK_MIMETYPES)
        for filename in mimetypes.knownfiles:
            if os.path.isfile(filename):
                self.mimedb.read(filename)
        self.mimedb.read_windows_registry()

        if magic is not None:
            self.magicdb = magic.open(magic.MIME_TYPE)
            if self.magicdb.load() != 0:
                self.magicdb = None
        else:
            self.magicdb = None

        if self.magicdb is None:
            self._get_mime_via_magic = lambda path: (None, '')
        self.py2warning = False
    
    @staticmethod
    def _split_mime(mimetype):
        if not mimetype:
            return None, ''
        else:
            cat, guess = mimetype.split('/', 1)
            return cat, MAPPINGS.get(guess, guess)

    def _get_mime_from_url(self, path):
        return self._split_mime(self.mimedb.guess_type(path)[0])

    def _get_mime_via_magic(self, path): # Occasionally replaced by stub
        return self._split_mime(self.magicdb.file(path))

    def __get_mime(self, path):
        catmagic, guessmagic = self._get_mime_via_magic(path)
        catext, guessext = self._get_mime_from_url(path)
        # `cat' is for `category'
        # Every source code undergoes MIME text/x-*; so,
        # we prefer category `text' over others.
        if catmagic == 'text':
            if catext != 'text':
                return guessmagic
            else:
                return guessext if guessext in KNOWN_MIMES else guessmagic
                # It turns out that libmagic is sometimes really stupid about small
                # code snippets.
                # TODO: write fast L(1) approximations to grammars of all languages.
                # Will be hard for TeX with changing character classes.
        else:
            # something is wrong here
            if guessmagic == 'octet-stream':
                # not even a text
                return None
            if catext == 'text':
                return guessext
            return None

    def __by_mime(self, fn):
        mime = self.__get_mime(fn)
        return KNOWN_MIMES.get(mime, None)

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
                ".tex" : "?latex"
                 }
        if (ext in dct):
            return dct[ext]
        else:
            return None

    def __proceed_python(self, path):
        with open(path, 'rb') as f:
            line = f.readline()
        if b"python3" in line: # much faster, proven by python -m timeit
            return "python3"
        elif b"python2" in line:
            return "python2"
        elif self.py2warning:
            return "python2"
        else:
            logger.warning("Assuming " + path + " is python2 file. \nIf you want to translate it with python3, insert 'python3' in the comment in the first line of this file")
            self.py2warning = True
            return "python2"

    def __by_contents(self, path, info):
        if (info[1:] == "python"):
            return self.__proceed_python(path)
        else:
            return None

    def get(self, path):
        """Returns None if no language supported"""
        res_by_mime = self.__by_mime(path)
        if res_by_mime is None or res_by_mime[0] != '?':
            return res_by_mime
        if not os.path.isfile(path):
            raise PleaseException("There is no file " + path) # XXX incorrect error message
        res_by_content = self.__by_contents(path, res_by_mime)
        return res_by_content

_lang = Language() # STOP INSTANTIATING IN EVERY FUNCTION CALL!

def get(path):
    '''Get a programming language for a file.'''
    return _lang.get(path)

def is_source_code(path):
    lang = get(path)
    return lang is not None and lang in langs # hey, there is TeX!

