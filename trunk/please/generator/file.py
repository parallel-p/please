#!/usr/bin/python

class File(object):
    """Reperesents .please file"""
    
    def __init__(self, file):
        self.file = file
        f = open(file, "r")
        self.script = f.readlines()
