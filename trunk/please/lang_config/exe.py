import os.path
from .base import BaseConfig

LANGUAGE = "executable"

class ExeConfig(BaseConfig):
    def run_command(self, source):
        return [source]

def get_config():
    return ExeConfigurator()
