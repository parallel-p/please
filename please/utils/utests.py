import os
from .. import globalconfig


def get_tests(basedir=globalconfig.temp_tests_dir):
    count = 1
    while(os.path.exists(os.path.join(basedir, str(count)))):
        yield os.path.join(basedir, str(count))
        count += 1
