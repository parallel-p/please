import os.path
from .base import BaseConfig

LANGUAGE = "command"

class CommandConfig(BaseConfig):
    def run_command(self, source):
        return [source]

    def get_binary_name(self, source):
        return [source]

def get_config():
    return CommandConfig
