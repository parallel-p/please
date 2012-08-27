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

class DprFreePascalConfig(DprBaseConfig):
    requirements = utils.exists('fpc')
    def _get_compile_commands(self, source):
        return (['fpc', '-Mdelphi', source], )

class DprDelphiConfig(DprBaseConfig):
    requirements = utils.is_windows() and utils.exists('dcc32.exe')
    def _get_compile_commands(self, source):
        return (["dcc32.exe", "-cc", source], )

def get_config():
    return utils.choose(DprDelphiConfig, DprFreePascalConfig)
# TODO add support for Kylix, more universal tests, etc.

