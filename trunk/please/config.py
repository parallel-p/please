#!/usr/bin/python

"""Configuration."""

import os.path
from . import configobj

class Config(object):
    def __init__(self):
        self.config = configobj.ConfigObj(os.path.join(self.scriptDir(), "please.ini"))
        
    def scriptDir(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) # TODO: is there a normal way to to this? -- PK
        
    def pleaseDir(self):
        return self.config.get('please-directory',".please");

    def problemFile(self):
        return self.config.get('problem-file',"default.package");

    def testsDir(self):
        return self.config.get('tests-directory',"tests");

    def generateFile(self):
        return os.path.join(self.testsDir(), 
              self.config.get('generate-file',"generate.please"));

config = Config() # TODO: I suspect it is not the right way to do this -- PK
