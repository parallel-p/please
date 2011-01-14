#!/usr/bin/python

"""Logging utilities."""

# TODO(dgozman): nothing implemented here.

class Log(object):
    pass

class ConsoleLog(object):
    def info(self, message):
        print message

    def error(self, message):
        print '[error] %s' % message

    def debug(self, message):
        print '[debug] %s' % message

