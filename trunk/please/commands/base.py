#!/usr/bin/python

"""Base commands."""

from .. import exceptions
from .. import locale
from .. import run
from .. import sourcefile
from .. import sandbox
from .. import file_system
from . import options

ALL_COMMANDS = set([])

class Command(object):
    """Command is an action performed by please tool.
    Only one command can be run at a time. Commands are specific to contexts.
    """
    
    NAMES = ''
    OPTIONS = []

    @classmethod
    def names(cls):
        if len(cls.NAMES) == 0:
            return ''
        if len(cls.NAMES) == 1:
            return cls.NAMES[0]
        return '{0} ({1})'.format(cls.NAMES[0], ', '.join(cls.NAMES[1:]))
    
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
    

class Help(Command):
    NAMES = ['help', 'h', '?']
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
            if name in c.NAMES:
                command = c
        
        if command is None:
            message = locale.get('unknown-command-in-context').format(
                command=name, context=self.context.NAME)
            if self.options.all:
                message = locale.get('unknown-command').format(name)
            raise exceptions.UserInputError(message, None)

        self.context.log.info('')
        self.context.log.info('{0}: {1}'.format(
            command.names(), command.description()))
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
        self.context.log.info(locale.get('commands.help.general-header'))
        max_len = max([len(c.names()) for c in commands])
        fmt = '{0:' + str(max_len + 2) + '} {1}'
        for c in sorted(commands, key=lambda c: c.names()):
            self.context.log.info(fmt.format(c.names(), c.description()))
        
    def print_general_options(self):
        self.context.log.info(locale.get('commands.help.general-options'))


class Update(Command):
    NAMES = ['update']
    
    def handle(self):
        self.context.log.info('This is an update command.')


class Run(Command):
    NAMES = ['run']

    @classmethod
    def usage(cls):
        return locale.get('commands.run.usage')
    
    @classmethod
    def description(cls):
        return locale.get('commands.run.description')

    def handle(self):
        if len(self.args) > 1:
            raise exceptions.UserInputError(
                locale.get('too-much-arguments'), self)
        if not self.args:
            raise exceptions.UserInputError(
                locale.get('not-enough-arguments'), self)

        executable = self.args[0]
        self.context.log.info("executable = " + str(executable))
        invoker = run.Invoker()
        result = invoker(executable)
        self.context.log.info("run: " + str(executable))
        self.context.log.info("time: %.3f sec" % result.timepeak)
        self.context.log.info("memory: %.3f MB" % (result.memorypeak / (1024.0 * 1024.0)))

class Compile(Command):
    NAMES = ['compile']

    @classmethod
    def usage(cls):
        return locale.get('commands.compile.usage')
    
    @classmethod
    def description(cls):
        return locale.get('commands.compile.description')

    def handle(self):
        log = self.context.log
        fs = self.context.file_system
           
        if len(self.args) > 1:
            raise exceptions.UserInputError(
                locale.get('too-much-arguments'), self)
        if not self.args:
            raise exceptions.UserInputError(
                locale.get('not-enough-arguments'), self)
        filename = self.args[0]
                
        log.info(locale.get('commands.compile.doing').format( #TODO: probably make a Command.doing() function or something
            filename) + "...")

        sb = sandbox.Sandbox("compile")
        sb.push(filename)
        sf = sourcefile.SourceFile(filename, sb)        
        sf.compile()

        # TODO: probably make a Command.popResult() function, as the following code is widely used in several commands
        outputDir = ".please/compile-ready" # TODO: use config
        fs.del_dir(outputDir)
        fs.mkdir(outputDir)
        sb.pop(sf.executable(), outputDir)

        log.info(locale.get('commands.compile.doing').format(filename) + 
                 ": " + locale.get('done') + "! " + 
                 locale.get('see-dir').format(outputDir)
          )
