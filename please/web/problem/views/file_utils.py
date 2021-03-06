import os

def norm(path):
    ''' 
    Normalize path: uses / instead \ , no / at the end.
    '''
    path = path.replace('\\', '/').replace('/./','/').rstrip('/')
    # WIN hack:
    if len(path) > 1 and path[1] == ':': # C:/...
       path = path.lower()

    return path

class ChangeDir:
    def __init__(self, path):
        self.old_path = os.getcwd()
        self.where = path

    def __enter__(self):
        if self.where:
            os.chdir(self.where)
        return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.old_path)


def list_files_flat(startpath):
    with ChangeDir(startpath):
        for root, dirs, files in os.walk('.'):
            for file in files:
                path = os.path.join(root, file)[2:]
                if path[0] != '.':
                    # print(norm(path))
                    yield norm(path)


def file_save(temp_file, path):
    name = os.path.join(path, temp_file.name)
    with open(name, 'wb') as destination:
        for chunk in temp_file.chunks():
            destination.write(chunk)
    return name


def file_write(text, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as source:
        source.write(text)


def file_read(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as destination:
        return destination.read()
