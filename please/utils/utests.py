import os

def get_tests(basedir):
    count = 1
    while(os.path.exists(os.path.join(basedir, str(count)))):
        yield os.path.join(basedir, str(count))
        count += 1