import shutil
import os

def clean():
    for file in os.listdir('.'):
        if (file[:4] == 'tmp_'):
            os.remove(file)
