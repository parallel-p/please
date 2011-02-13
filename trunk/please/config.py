#!/usr/bin/python

"""Configuration."""

import os
import os.path
from . import configobj

class Config(object):
    #All the paths that point to a particular object (like scriptDir or texPrologue) 
    #are returned relative to current dir. Probably we will need to change this, but think first. -- PK
    def __init__(self):
        self.config = configobj.ConfigObj(os.path.join(self.pleaseiniDir(), "please.ini"))
        
    def scriptDir(self):
        return os.path.relpath(os.path.join(os.path.dirname(__file__), "..")) # TODO: is there a normal way to to this? -- PK
        
    def pleaseiniDir(self):  # TODO: change if we will support several please.ini files
        return self.scriptDir()
        
    def pleaseDir(self):
        return self.config.get('please-directory', ".please")

    def problemFile(self):
        return self.config.get('problem-file', "default.package")

    def testsDir(self):
        return self.config.get('tests-directory', "tests")

    def generateFile(self):
        return os.path.join(self.testsDir(), 
              self.config.get('generate-file', "generate.please"))
    
    def workDir(self):
        return os.path.join(self.pleaseDir(),
                self.config.get('work-directory', 'work'))
               
    def statementsReadyDir(self):
       return os.path.join(self.pleaseDir(),
                self.config.get('statements-ready-directory', 'statements-ready'))
                
    def texPrologue(self, forTeX = False): # Is there a way to make it accessible as config.tex.prologue() ? -- PK
        """tex.prologue returns the file with TeX prologue.
        forTex means: if false, return the path with slashes as needed by current OS;
                      if true, return path with / as separators (as required by TeX)
        """
        try:
            prlg = self.config['tex']['prologue'] # can we use get() here (it is the second-level parameter) -- PK
        except KeyError:
            prlg = "_prologue.tex"
            
        prlg = os.path.join(self.pleaseiniDir(), prlg)
        if forTeX and (os.name == "nt"):
            prlg = prlg.replace("\\", "/")
        return prlg
        
    def texCommands(self):
        try:
           cmd = self.config['tex']['commands']
        except KeyError:
           cmd = {}
           
        if not cmd:
           cmd = {1: 'latex', 2: 'latex', 3: 'dvips', 4: 'dvipdfm'}
        return list(cmd.values())
        
config = Config() # TODO: I suspect it is not the right way to do this -- PK
