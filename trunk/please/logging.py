#!/usr/bin/python

"""Logging utilities."""

from . import locale

import os

DEBUG, INFO, NOTICE, WARNING, ERROR, FATAL, NO_LOGGING = range(7)

_MESSAGES = {
    DEBUG: locale.get('log.debug'),
    INFO: locale.get('log.info'),
    NOTICE: locale.get('log.notice'),
    WARNING: locale.get('log.warning'),
    ERROR: locale.get('log.error'),
    FATAL: locale.get('log.fatal'),
    NO_LOGGING: ''
    }


class Log(object):
    def __init__(self):
        self.debug = lambda text: self.log(DEBUG, text)
        self.info = lambda text: self.log(INFO, text)
        self.notice = lambda text: self.log(NOTICE, text)
        self.warning = lambda text: self.log(WARNING, text)
        self.error = lambda text: self.log(ERROR, text)
        self.fatal = lambda text: self.log(FATAL, text)
        self.level = DEBUG
        
    def log(self, level, message, end='\n'):
        if level < self.level:
            return
        if level != INFO:
            message = '[{0}] {1}'.format(_MESSAGES[level], message)
        self.write(level, message, end)
        
    def write(self, level, message, end):
        pass
    
if os.name == 'posix':
    class ConsoleLog(Log):
        _COLORS = {
            DEBUG: 36, INFO: 22, NOTICE: 32, WARNING: 33, ERROR: 31, FATAL: 31,
            NO_LOGGING: 30
            }
    
        def write(self, level, message, end):
            message = "\x1b[1;%dm%s\x1b[0m" % (self._COLORS[level], message)
            print(message, end=end)

elif os.name == 'nt':
    import ctypes
    class ConsoleLog(Log):
        STD_OUTPUT_HANDLE = ctypes.windll.kernel32.GetStdHandle(-11)

        _COLORS = {
            DEBUG: 11, INFO: 7, NOTICE: 2, WARNING: 14, ERROR: 12, FATAL: 4,
            NO_LOGGING: 0
            }
    
        def write(self, level, message, end):
            ctypes.windll.kernel32.SetConsoleTextAttribute(
                self.STD_OUTPUT_HANDLE, self._COLORS[level])
            print(message, end=end)

