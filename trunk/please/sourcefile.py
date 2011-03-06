#!/usr/bin/python

"""
Sourcefile handles everything about compiling and execiting a given source file
"""

import os.path
from . import config
from . import sandbox
from . import exceptions

class SourceFile(object):
    def __init__(self, filename, sandbox):
        self.filename, self.lang = os.path.splitext(filename)
        if self.lang != ".pas": # TODO: load list of languages from config; and use all the parameters below
            raise exceptions.UnknownLanguageError(self.lang, filename)
        self.sandbox = sandbox
            
    def compile(self):
        self.sandbox.exec("fpc","-Mdelphi " + self.filename +  self.lang) # TODO: check return value
        
    def executable(self):
        if os.name == "posix":
            return self.filename
        elif os.name == "nt":
            return self.filename + ".exe"
        
    
        
