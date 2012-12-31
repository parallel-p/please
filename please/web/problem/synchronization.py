from please.package.config import Config
import os

def import_to_database(path):
    os.chdir(path)
    config = Config(open("default.package", "r").read())

    return config
