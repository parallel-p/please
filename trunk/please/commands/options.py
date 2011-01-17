#!/usr/bin/python

"""Options for commands."""

from .. import locale

import optparse
import sys

class OptionParser(optparse.OptionParser):
    def __init__(self, log, command):
        optparse.OptionParser.__init__(self)
        self.log = log
        self.command = command
        
    def error(self, message):
        self.log.error(message)
        self.log.info(locale.get('options.use-help').format(self.command.NAME))
        sys.exit(2)


class Option(object):
    def __init__(self, name, usage_callback, parser_option):
        self.name = name
        self.usage_callback = usage_callback
        self.parser_option = parser_option
        
    @staticmethod
    def usage_all():
        return locale.get('options.usage-all')


ALL_OPTIONS = [
    Option('all', Option.usage_all, optparse.make_option(
           '-a', '--all',
           action='store_true',
           dest='all',
           default=False)),
    ]
