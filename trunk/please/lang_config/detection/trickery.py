from .MAGIC_H import *

class Trickery:
    '''A non-magic magic stub.'''
    def __init__(self):
        pass

    def load(self, file = None):
        # I'm sorry.
        return 0

    def close(self):
        pass

    def file(self, path):
        return 'application/octet-stream'

def open(flags):
    return Trickery()
