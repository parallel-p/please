from .base import BaseConfig

LANGUAGE = "perl"

class PerlConfig(BaseConfig):
    def _get_run_command(self, source):
        return ["perl", source]

    def _get_binaries(self, source):
        return []
    

def get_config():
    return PerlConfig

MIMES = ["text/x-perl"]
EXTENSIONS = [".pl", ".pm"]
