#!/usr/bin/python

"""Different launch contexts of please tool.

Please can be run inside:
- well-formed problem directory,
- not well-formed problem directory (not in please format),
- well-formed contest directory,
- somewhere.
"""

from . import commands
from . import config
from . import locale

import os.path

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
        
    def __str__(self):
        return self.NAME + ' (' + self.directory + ')'
        
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
        
        self.log.error(locale.get('unknown-command-in-context').format( 
            command=args[0], context=self.NAME))
        
    @staticmethod
    def is_applicable(path):
        return False


class ProblemContext(Context):
    """Please-formatted problem context."""
    
    NAME = locale.get('context.problem.name')
    COMMANDS = [commands.HelpCommand]

    def __init__(self, directory, log):
        Context.__init__(self, directory, log)
        # Should have .problem field at least.

    @staticmethod
    def is_applicable(path):
        please_dir = os.path.join(path, config.PLEASE_WORK_DIR)
        problem_file = os.path.join(please_dir, config.PLEASE_PROBLEM_FILE)
        return (os.path.isdir(path) and os.path.isdir(please_dir) and
                os.path.isfile(problem_file))


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

    @staticmethod
    def is_applicable(path):
        return True


_CONTEXTS = [ProblemContext, ContestContext,
             SeemsLikeProblemContext, GlobalContext]

def guess(directory, log):
    for cls in _CONTEXTS:
        path = directory
        # TODO(dgozman): why 10? Go to the root?
        for _ in range(10):
            if cls.is_applicable(path):
                return cls(path, log)
            path = os.path.split(path)[0]
    return None

