import os
import zipfile
import shutil

def unzip(name, directory):
    """
    This method unzips polygon package.
    Problems are created in main Please directory. Method takes sole argument:
    package - path to polygon package to be extracted
    """
    prev_dir = os.getcwd()
    zf = zipfile.ZipFile(name)
    zf.extractall(directory)
    os.chdir(directory)
    for file in os.listdir('.'):
        if (file.find('\\') != -1):
            _file = file
            file = file.replace('\\', '/')
            path, who = os.path.split(file)
            try:
                os.mkdir(path)
            except OSError as e:
                if (e.errno != 17):
                    raise e
            shutil.move(_file, file)
    os.chdir(prev_dir)

