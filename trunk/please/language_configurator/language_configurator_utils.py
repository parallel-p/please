import sys

def is_windows():
    return sys.platform == 'win32' or sys.platform == 'cygwin'
