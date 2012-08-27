#/bin/python3
import os
import mimetypes

# Damn Apple.
USE_SYSTEM_SETTINGS = False

# Trying to access libmagic.
# libmagic is a library distributed with file(1) and commonly found on
# Linux distributions; it guesses type or MIME-type of file with searching
# of certain byte sequences within it.

try:
    from . import magic
except (OSError, ImportError):
    from . import trickery as magic
from . import trickery
MAGIC_FLAGS = magic.MIME_TYPE | magic.ERROR

class LanguageDetector:
    '''
    This class determines in which programming language given
    source code file is written.
    Currently it's very stupid, so don't mix extensions and
    don't be sad if it has made a mistake.

    Example:
    lang = LanguageDetector()
    print(lang().get("test_files/helloworld.pas")) # outputs pascal
    print(lang().get("test_files/helloworld3.py")) # outputs python
    '''

    def __init__(self):
        self._mimedb = mimetypes.MimeTypes()
        if USE_SYSTEM_SETTINGS:
            for filename in mimetypes.knownfiles:
                if os.path.isfile(filename):
                    self._mimedb.read(filename)
            self.mimedb.read_windows_registry()

        self._magicdb = magic.open(MAGIC_FLAGS)
        if self._magicdb.load() != 0:
            self._magicdb.close()
            self._magicdb = trickery.open(MAGIC_FLAGS)
            self._magicdb.load()

        self._mimes = {}

    @staticmethod
    def _split_mime(mimetype):
        if not mimetype:
            return '', '', mimetype
        else:
            try:
                cat, guess = mimetype.split('/', 1)
            except ValueError:
                assert 0, mimetype + 'is not mime type'
            return cat, guess, mimetype

    def _get_mime_from_url(self, path):
        return self._split_mime(self._mimedb.guess_type(path)[0])

    def _get_mime_via_magic(self, path): # Occasionally replaced by stub
        return self._split_mime(self._magicdb.file(path))

    def __get_mime(self, path):
        catmagic, guessmagic, mimemagic = self._get_mime_via_magic(path)
        catext, guessext, mimeext = self._get_mime_from_url(path)
        # `cat' is for `category'
        # Every source code undergoes MIME text/x-*; so,
        # we prefer category `text' over others.
        if catmagic == 'text':
            if catext != 'text':
                return mimemagic
            else:
                return mimeext if mimeext in self._mimes else mimemagic
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
                return mimeext
            return None

    def __by_mime(self, fn):
        mime = self.__get_mime(fn)
        return self._mimes.get(mime, None)

    def __proceed_brainfuck(self, path):
        useable_bytes = set(b'<>[]+-')
        total = 0
        useable = 0
        balance = 0
        left = ord('[')
        right = ord(']')
        valid = True
        with open(path, 'rb') as f:
            while True:
                chunk = tuple(f.read(1024))
                if not chunk:
                    break
                total += len(chunk)
                for byte in chunk:
                    if byte in useable_bytes:
                        useable += 1
                        if byte == left:
                            balance += 1
                        elif byte == right:
                            balance -= 1
                            if balance < 0:
                                valid = False
                                break
        valid &= (balance == 0)
        if useable and (10 * useable >= 9 * total or 2 * useable >= total and valid):
            return "brainfuck"
        return None

    def get_name(self, path):
        """Returns None if no language supported"""
        return self.__by_mime(path)

    def _add_module(self, mod):
        for mime in mod.MIMES:
            self._mimes[mime] = mod.LANGUAGE
        MIME = mod.MIMES[0]
        for ext in mod.EXTENSIONS:
            self._mimedb.add_type(MIME, ext)
