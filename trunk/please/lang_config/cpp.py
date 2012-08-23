import os.path
from . import utils
from .base import BaseConfig

LANGUAGE = "c++"
MIMES = ["text/x-c++", "text/x-c++hdr", "text/x-c++src"]
EXTENSIONS = [".c++", ".cpp", ".cxx", ".cc",
              ".h++", ".hpp", ".hxx", ".hh"]

class CppNixConfig(BaseConfig):
    def _get_compile_commands(self, source):
        return (["g++", "-lm", "-s", "-x", "c++",
        "-O2", "-o", os.path.splitext(source)[0], source],
               )

    def _get_run_command(self, source):
        if "/" not in source:
            source = "./" + source
        return [os.path.splitext(source)[0]]
    
    def _get_binaries(self, source):
        return [os.path.splitext(source)[0]]

class CppWindowsConfig(BaseConfig):
    def _get_compile_commands(self, source):
        return (["g++", "-lm", "-s", "-x", "c++",
        "-O2",
        "-o", os.path.splitext(source)[0] + ".exe",  source],)
    
    def _get_run_command(self, source):
        return [os.path.splitext(source)[0] + ".exe"]

    def _get_binaries(self, source):
        return [os.path.splitext(source)[0] + ".exe"]

def get_config():
    ''' Returns configurator object depends on OS you run  '''
    if utils.is_windows():
        return CppWindowsConfig
    else:
        return CppNixConfig
