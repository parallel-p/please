"""Bindings for libmagic."""

from ctypes import cdll
import ctypes
from ctypes.util import find_library

from .MAGIC_H import *

_path = find_library('magic')

if not _path:
    raise ImportError('magic.py rendered unusable')

_libmagic = cdll.LoadLibrary(_path)

magic_set = type('magic_set', (ctypes.Structure,), {})
magic_t = ctypes.POINTER(magic_set)

_open = _libmagic.magic_open
_open.restype = magic_t
_open.argtypes = [ctypes.c_int]

_close = _libmagic.magic_close
_close.restype = None
_close.argtypes = [magic_t]

_file = _libmagic.magic_file
_file.restype = ctypes.c_char_p
_file.argtypes = [magic_t, ctypes.c_char_p]

_load = _libmagic.magic_load
_load.restype = ctypes.c_int
_load.argtypes = [magic_t, ctypes.c_char_p]

class Magic:
    def __init__(self, ms):
        self.handle = ms


    def load(self, file = None):
        if file is not None:
            file = file.encode()
        return _load(self.handle, file)

    def close(self):
        _close(self.handle)

    def file(self, path):
        if isinstance(path, str):
            path = path.encode()
        answer = _file(self.handle, path)
        return answer.decode('ascii') if answer is not None else None


def open(flags):
    return Magic(_open(flags))
