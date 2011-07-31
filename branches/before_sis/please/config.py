#!/usr/bin/python

"""Configuration."""

import os
import os.path
from .third_party import configobj
from . import locale

class LanguageConfig(object):
    """Stores the parameters of a given language"""
    # TODO: a better realization is required
    def __init__(self, compileFormat, runFormat):
        self.compileFormat = compileFormat
        self.runFormat = runFormat
       
    def compileLine(self, file, outputFile):
        baseName = os.path.splitext(file)[0]
        return self.compileFormat.format(baseName, file, outputFile)
        
    def runLine(self, file, outputFile):
        baseName = os.path.splitext(file)[0]
        if self.runFormat == "":
            return os.path.join(".", outputFile) # assuming the file is in the current dir
        else:
            return self.runFormat.format(baseName, file, outputFile)

class Config(object):
    #All the paths that point to a particular object (like scriptDir or texPrologue) 
    #are returned relative to current dir. Probably we will need to change this, but think first. -- PK
    def __init__(self):
        self.config = configobj.ConfigObj(os.path.join(self.pleaseiniDir(), "please.ini"))
        
        try:
            langs = set(self.config["compilers"].keys())
        except KeyError: langs = set([])
        try:
            langs = langs | set(self.config["executers"].keys())
        except KeyError: pass
        self.lang = dict()
        for lang in langs:
            comp = self.config["compilers"].get(lang, "");
            run = self.config["executers"].get(lang, "");
            self.lang[lang] = LanguageConfig(comp, run)
        
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
                
    def testsReadyDir(self):
       return os.path.join(self.pleaseDir(),
                self.config.get('tests-ready-directory', 'tests-ready'))
                
    def inputFormat(self):
       return self.config.get('input-format', '%02d')
                
    def answerFormat(self):
       return self.config.get('answer-format', '%02d.a')
                
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

    def texFiles(self):
        try:
           fl = self.config['tex']['files']
        except KeyError:
           fl = {}
        res = []
        for file in fl.values():
            res.append(os.path.join(self.pleaseiniDir(), file))
        return res
        
    def languageConfig(self, lang):
        """Return the configuration for language lang. Throws KeyError if no such language"""
        return self.lang[lang]; 

config = Config() # TODO: I suspect it is not the right way to do this -- PK
