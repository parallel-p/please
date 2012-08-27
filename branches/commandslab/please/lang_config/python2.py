from .base import BaseConfig

LANGUAGE = "python2"

class Python2Config(BaseConfig):
    def _get_run_command(self, source):
        return ["python", "-O", source]
    
    def is_run_garbage(self, path):
        return path.endswith(".pyc")

def get_config():
    return Python2Config
