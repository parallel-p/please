#!/usr/bin/python

"""Different launch contexts of please tool.

Please can be run inside:
- well-formed problem directory,
- not well-formed problem directory (not in please format),
- well-formed contest directory,
- somewhere.
"""

from . import commands
from . import locale

class Context(object):
    """Context defines what can be done in the particular directory.
    It also encapsulates some globals like log, problem instance, etc.
    """
    
    # Name to be used in logging.
    NAME = ''
    # All available commands for this context.
    COMMANDS = []
    
    def __init__(self, directory, log):
        self.directory = directory
        self.log = log
        
    def handle(self, args):
        if not args:
            commands.HelpCommand(self, args).handle()
            return
        
        command = None
        for command_cls in self.COMMANDS:
            if command_cls.NAME == args[0]:
                command = command_cls(self, args[1:])
        if command:
            command.handle()
            return
        
        self.log.error(locale.get('contexts.unknown-command-in-context') % 
                       {'command': args[0], 'context': self.NAME})


class ProblemContext(Context):
    """Please-formatted problem context."""
    
    # Should have .problem field at least.
    pass


class SeemsLikeProblemContext(Context):
    """Not please-formatted problem context. Intended to be used for import."""
    
    # Probably will have .problem field.
    pass


class ContestContext(Context):
    """Please-formatted contest context."""
    
    # Should have .contest field at least.
    pass


class GlobalContext(Context):
    """Context 'somewhere'."""
    
    NAME = locale.get('context.global.name')
    COMMANDS = [commands.HelpCommand, commands.UpdateCommand]


def guess(directory, log):
    # TODO(dgozman): implement this
    return GlobalContext(directory, log)

