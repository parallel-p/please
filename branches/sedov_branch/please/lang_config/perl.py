from .base import BaseConfig

LANGUAGE = "perl"
MIMES = ["text/x-perl"]
EXTENSIONS = [".pl", ".pm"]

class PerlConfig(BaseConfig):
    def _get_run_command(self, source):
        return ["perl", source]
    

def get_config():
    return PerlConfig
