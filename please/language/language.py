#/bin/python3
import os
import logging
import re
from ..utils.exceptions import PleaseException

#"" is for commands
langs = ["c", "c++", "c#", "pascal", "delphi", "python2", "python3", "java", ""]


# Trying to access libmagic.
# libmagic is a library distributed with file(1) and commonly found on
# Linux distributions; it guesses type or MIME-type of file with searching
# of certain byte sequences within it.

try:
    from . import magic
    raise OSError
    _mresolv = magic.open(magic.MIME)
    if _mresolv.load():
        raise OSError
except (OSError, ImportError):
    def magic_guess(filename):
        return None
else:
    def magic_guess(filename):
        s = _mresolv.file(filename.encode())
        if s:
            return s.decode().split(';', 1)[0]
        return None

import mimetypes
_mimedb = mimetypes.MimeTypes()
fallback_path = os.path.join(os.path.dirname(__file__), 'mime.types')
if os.path.isfile(fallback_path):
    _mimedb.read(fallback_path)
for file in mimetypes.knownfiles:
    if os.path.isfile(file):
        _mimedb.read(file)
_mimedb.read_windows_registry()

def mime_guess(url):
    return _mimedb.guess_type(url)[0]

_mappings = { # mappings for some MIME synonyms
    'x-csrc': 'x-c',
    'x-chdr': 'x-c',
    'x-c++src': 'x-c++',
    'x-c++hdr': 'x-c++',
}

_known_mimes = { # all MIMES that we are interested in
    'x-c': 'c', 
    'x-c++': 'c++',
    'x-csharp': 'c#',
    'x-pascal': 'pascal',
    'x-delphi': 'delphi',
    'x-python': '?python',
    'x-java': 'java',
    'x-tex': '?latex',
    'x-empty': None,
}

#_problematic_pairs = { # set of pairs (<possible wrong libmagic guess>, <true guess>)
#    ('x-c', 'x-c++'),
#    ('x-c', 'x-csharp'),
#    ('x-c++', 'x-csharp'),
#    ('x-pascal', 'x-delphi'),
#}

def _as_cat_guess(mimetype):
    if not mimetype:
        return None, ''
    else:
        cat, guess = mimetype.split('/', 1)
        return cat, _mappings.get(guess, guess)

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

    def __get_mime(self, fn):
        catmagic, guessmagic = _as_cat_guess(magic_guess(fn))
        catext, guessext = _as_cat_guess(mime_guess(fn))
        # `cat' is for `category'
        # Every source code undergoes MIME text/x-*; so,
        # we prefer category `text' over others.
        if catmagic == 'text':
            if catext != 'text':
                return guessmagic
            else:
                return guessext if guessext in _known_mimes else guessmagic
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
        return _known_mimes.get(mime, None)


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
        if b'python3' in line:
            return "python3"
        elif b'python2' in line:
            return "python2"
        else:
            log = logging.getLogger("please_logger.language")
            log.warning("Assuming " + path + " is python2 file. \nIf you want to translate it with python3, insert 'python3' in the comment in the first line of this file")
            return "python2"

    def __proceed_latex(self, path):
        with open(path, 'rb') as f:
            content = f.read()
        if re.compile(b'\\includegraphics[^{]*\{[^}]*\.(?:png|jpe?g|pdf)\}').search(content):
            return "latex_pdf"
        else:
            return "latex_ps"

    def __by_contents(self, path, info):
        if (info[1:] == "python"):
            return self.__proceed_python(path)
        if (info[1:] == "latex"):
            return self.__proceed_latex(path)
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

def is_source_code(path):
    detector = Language()
    lang = detector.get(path)
    return lang is not None and lang in langs # hey, there is TeX!

