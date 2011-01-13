#!/usr/bin/python

"""Logging utilities."""

class Log(object):
    pass

class ConsoleLog(object):
    def info(self, message):
        print message

    error = info
    pass

