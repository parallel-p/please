import re

REGEXP = re.compile(r'(\D+)')

def testfile_sorting_key(testfile):
    fname = getattr(testfile, 'filename', '')
    return sorting_key(fname)

def sorting_key(fname):
    return tuple((int(item) if item.isdigit() else item)
                 for item in REGEXP.split(fname) if item)

