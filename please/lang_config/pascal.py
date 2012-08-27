import os
import os.path
from . import utils
from .base import BaseConfig

LANGUAGE = "pascal"

class FPCConfig(BaseConfig):
    requirements = utils.exists('fpc')
    def _get_compile_commands(self, source):
        return (['fpc', '-Mfpc', source], )

    def is_compile_garbage(self, source):
        extensions = {".obj", ".o"}

        extension = os.path.splitext(source)[1]
        return extension.lower() in extensions

def get_config():
    return utils.choose(FPCConfig)
# TODO add support for Borland Pascal

