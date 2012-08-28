from .base import BaseConfig
import sys

LANGUAGE = "python3"

class Python3Config(BaseConfig):
    def _get_run_command(self, source):
        return ['python', '-O', source]

    def is_run_garbage(self, path):
        return path.endswith('.pyc')

    def _get_binaries(self, source):
        return []

def get_config():
    return Python3Config

