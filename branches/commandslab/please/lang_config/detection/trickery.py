from .MAGIC_H import *
import builtins


_BINARY = 'application/octet-stream'
_TEXT = 'text/plain'
_CHUNK = 4096

class Trickery:
    '''A non-magic magic stub.'''
    def __init__(self):
        pass

    def load(self, file = None):
        # I'm sorry.
        return 0

    def close(self):
        pass

    def file(self, path):
        try:
            with builtins.open(path, 'rb') as fp:
                chunk = fp.read(_CHUNK)
        except (IOError, OSError):
            return ''
        if 0 in chunk:
            return _BINARY
        else:
            return _TEXT

def open(flags):
    return Trickery()
