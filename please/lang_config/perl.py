from .base import BaseConfig

LANGUAGE = "perl"

class PerlConfig(BaseConfig):
    def _get_run_command(self, source):
        return ["perl", source]
    

def get_config():
    return PerlConfig

MIMES = ["text/x-perl"]
EXTENSIONS = [".pl", ".pm"]