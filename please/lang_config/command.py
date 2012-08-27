import os.path
from .base import BaseConfig
from .utils import exe_suffix, is_windows

LANGUAGE = "command"

if is_windows():
    MIMES = ["application/x-executable"]
else:
    MIMES = ["application/x-dosexec"]

EXTENSIONS = [exe_suffix]

class CommandConfig(BaseConfig):
    def run_command(self, source):
        return [source]

    def get_binary_name(self, source):
        return [source]

def get_config():
    return CommandConfig
