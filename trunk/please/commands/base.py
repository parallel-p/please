#!/usr/bin/python

"""Base commands."""

from .. import locale

class Command(object):
    """Command is an action performed by please tool.
    Only one command can be run at a time. Commands are specific to contexts.
    """
    
    NAME = ''
    
    def __init__(self, context, args):
        self.context = context
        self.args = args
    
    def handle(self):
        pass


class HelpCommand(Command):
    NAME = locale.get('commands.help.name')
    
    def handle(self):
        self.context.log.info('This is a help command.')


class UpdateCommand(Command):
    NAME = locale.get('commands.update.name')
    
    def handle(self):
        self.context.log.info('This is an update command.')
