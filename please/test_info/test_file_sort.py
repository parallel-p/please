import re

def sorting_key(file):
    result = []
    for item in re.split(r'(\D{1,})', file):
        if item == "": continue
        if item.isdigit():
            item = int(item)
        result.append(item)

    return result
