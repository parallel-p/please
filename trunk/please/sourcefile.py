#!/usr/bin/python

"""
Sourcefile handles everything about compiling and execiting a given source file
"""

import os.path
from . import config
from . import sandbox
from . import exceptions
from . import file_system

#TODO: rework for non-compiled languages
class SourceFile(object):
    def __init__(self, filename, sandbox):
        self.fileName, self.lang = os.path.splitext(filename)
        try:
            self.langConfig = config.config.lang[self.lang];
        except KeyError:
            raise exception.UnknownLanguageError(self.lang, filename)
        self.sandbox = sandbox
        self.fs = file_system.FileSystem()
            
    def compile(self):
        self.sandbox.exec(self.langConfig.compileLine(
            self.fileName + self.lang, 
            self.executable()            
        )) # TODO: check return value
        
    def executable(self):
        return self.fileName + self.fs.binarySuffix()
        
    def run(self):
        self.sandbox.exec(self.langConfig.runLine(
            self.executable()
        )) # TODO: check return value
        
        
