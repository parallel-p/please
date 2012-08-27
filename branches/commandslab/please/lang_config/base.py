"""Base class for language configurators."""
from . import utils # sane assumptions

class BaseConfig:
    '''Class that provides common config for handling a filetype.'''
    def __init__(self, source):
        self._setup()
        self.compile_commands = self._get_compile_commands(source)
        self.run_command = self._get_run_command(source)
        self.environment = self._get_environment(source)
        self.binaries = self._get_binaries(source)
        self.source = source

    def _setup(self):
        '''Acquire information about outer space.'''
        pass

    def _get_compile_commands(self, source) -> (list,):
        '''Returns a sequence of commands represented by lists that
        need to be executed to compile a file.'''
        return ()

    def _get_run_command(self, source) -> list:
        '''Returns a command that runs a source or its compilation result.'''
        return [utils.run_command(source)]
    
    def _get_environment(self, source) -> dict:
        '''Return an environment variables that need to be set to compile/run
        a file.'''
        return {}

    def is_compile_garbage(self, path) -> bool:
        '''Tests if certain file is side-effect of compilation.'''
        return False

    def is_run_garbage(self, path) -> bool:
        '''Tests if certain file is side-effect of running.'''
        return False

    def _get_binaries(self, source) -> list:
        '''Returns a list of paths that will be (were) made as results
        of compiling source.'''
        return [utils.run_command(source)]
