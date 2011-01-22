#!/usr/bin/python

"""Base commands."""

from .. import locale
from . import options

ALL_COMMANDS = []

class Command(object):
    """Command is an action performed by please tool.
    Only one command can be run at a time. Commands are specific to contexts.
    """
    
    NAME = ''
    OPTIONS = []
    
    @classmethod
    def usage(cls):
        return ('usage: please command ARG1 ARG2 [options]\n'
                'Something useful will be done with ARG1 and ARG2.')
    
    @classmethod
    def description(cls):
        return 'Does something useful.'

    def __init__(self, context, args):
        self.context = context
        self.args = args
        parser = options.OptionParser(self.context.log, self)
        for option in options.ALL_OPTIONS:
            if option.name in self.OPTIONS:
                parser.add_option(option.parser_option)
        self.options, self.args = parser.parse_args(args=args)
    
    def handle(self):
        pass    


class HelpCommand(Command):
    NAME = 'help'
    OPTIONS = ['all']
    
    @classmethod
    def usage(cls):
        return locale.get('commands.help.usage')
    
    @classmethod
    def description(cls):
        return locale.get('commands.help.description')

    def handle(self):
        commands = self.context.COMMANDS
        if self.options.all:
            commands = ALL_COMMANDS 
        
        if self.args:
            for name in self.args:
                self.handle_command(commands, name)
            
            self.context.log.info('')
            self.print_general_options()
        else:
            self.handle_general(commands)
            
    def handle_command(self, commands, name):
        command = None
        for c in commands:
            if c.NAME == name:
                command = c
        
        if command is None:
            message = locale.get('unknown-command-in-context').format(
                command=name, context=self.context.NAME)
            if self.options.all:
                message = locale.get('unknown-command').format(name)
            self.context.log.info(message)
            return

        self.context.log.info('')
        self.context.log.info('{0}: {1}'.format(
            command.NAME, command.description()))
        self.context.log.info(command.usage())
        
        if not command.OPTIONS:
            return
        
        self.context.log.info(locale.get('commands.help.valid-options'))
        for option in options.ALL_OPTIONS:
            if option.name in command.OPTIONS:
                usage = option.usage_callback()
                for line in usage.split('\n'):
                    self.context.log.info('  ' + line)
        
    def handle_general(self, commands):
        self.context.log.info(locale.get('help.general-header'))
        max_len = max([len(c.NAME) for c in commands])
        fmt = '{0:' + str(max_len + 2) + '} {1}'
        for c in commands:
            self.context.log.info(fmt.format(c.NAME, c.description()))
        
    def print_general_options(self):
        self.context.log.info(locale.get('commands.help.general-options'))


class UpdateCommand(Command):
    NAME = 'update'
    
    def handle(self):
        self.context.log.info('This is an update command.')

class CheckProblemCommand(Command):
    NAME = 'check'

    def validator(self, problem, fs):
        validator = problem.validator()
        if validator is None:
            from please.searcher.validator import Validator
            validator_file = Validator(fs).file()
            if validator_file is not None:
                from please.properties.validator import Validator
                validator = Validator(validator_file)

        return validator
    
    def checker(self, problem, fs):
        checker = problem.checker()
        if checker is None:
            from please.searcher.checker import Checker
            checker_file = Checker(fs).file()
            if checker_file is not None:
                from please.properties.checker import Checker
                checker = Checker(checker_file)

        return checker
    
    def handle(self):
        log = self.context.log
        log.info('Running check problem command.')
        from please.properties.problem import Problem
        from please.file_system import FileSystem
        fs = FileSystem(self.context.directory)
        problem = Problem(fs)
        
        validator = self.validator(problem, fs)
        if validator is not None:
            log.info("validator is found on path %s" % validator.file())
        else:
            log.warning("validator is not found")

        checker = self.checker(problem, fs)
        if checker is not None:
            log.info("checker is found on path %s" % checker.file())
        else:
            log.error("checker is not found")



