import os.path


def file_save(temp_file, path):
    name = os.path.join(path, temp_file.name)
    with open(name, 'wb') as destination:
        for chunk in temp_file.chunks():
            destination.write(chunk)
    return name
