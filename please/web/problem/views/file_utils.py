import os


class ChangeDir:
    def __init__(self, path):
        self.old_path = os.getcwd()
        self.where = path

    def __enter__(self):
        os.chdir(self.where)
        return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.old_path)


def list_files_flat(startpath):
    with ChangeDir(startpath):
        for root, dirs, files in os.walk('.'):
            for file in files:
                yield os.path.join(root, file)[2:]


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
