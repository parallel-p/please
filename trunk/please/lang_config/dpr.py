import os
import os.path
from . import utils
from .base import BaseConfig

LANGUAGE = "delphi"

class DprBaseConfig(BaseConfig):
    def is_compile_garbage(self, source):
        extensions = {".bpg", ".bpl", ".cfg", ".dcp", ".dcu",
            ".ddp", ".dfm", ".~df", ".dof", ".dpk", ".~dp", ".dsk",
            ".dsm", ".dci", ".dro", ".dmt", ".dct", ".obj", ".~pa",
            ".res", ".rc", ".todo", ".o", ".bak"}

        if os.path.splitext(source)[1] == '':
            return False

        extension = os.path.splitext(source)[1]
        return extension.lower() in extensions

    def is_run_garbage(self, source): #no garbage after running dpr project
        return False

class DprFreePascalConfig(DprBaseConfig):
    def _get_compile_commands(self, source):
        return (['fpc', '-Mdelphi', source], )

    def _get_run_command(self, source):
        if "/" not in source:
            source = "./" + source
        return [os.path.splitext(source)[0]]
    
    def _get_binaries(self, source):
        return [os.path.splitext(source)[0]]

class DprDelphiConfig(DprBaseConfig):
    def _get_compile_commands(self, source):
        return (["dcc32.exe", "-cc", source], )

    def _get_run_command(self, source):
        return [os.path.splitext(source)[0] + ".exe"]
    
    def _get_binaries(self, source):
        return [os.path.splitext(source)[0] + ".exe"]

def get_config():
    if utils.is_windows():
        return DprDelphiConfig
    else:
        return DprFreePascalConfig
# TODO add support for Kylix, more universal tests, etc.

