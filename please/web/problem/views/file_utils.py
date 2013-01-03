import os.path


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
