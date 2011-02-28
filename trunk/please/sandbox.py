#!/usr/bin/python

"""Sandbox allows to run commands and see what has changed
"""

import time
import os
from . import config
from . import file_system

class Sandbox(object):
    def __init__(self, name,  keep = False):
        """Creates a directory for sandbox. 
        name is an "identifier" to be used in directory name
        keep = True means do not delete sandbox directory even after the work is done
        """
        self.dirname = os.path.join(config.config.workDir(), 
                               name + time.strftime("_%Y%m%d_%H%M%S"))
        self.fs = file_system.FileSystem()
        self.fs.del_dir(self.dirname)
        self.fs.mkdir(self.dirname)
        self.mustKeep = keep
        self.files = set([])
        
    def __del__(self):
        if (not self.mustKeep):
            self.fs.del_dir(self.dirname)
            
    def keep(self,  newkeep = True):
        """ keep() means do not delete sandbox dir even after the work is done
        keep(false) means delete the directory after the work is done
        """
        self.mustKeep = newkeep
        
    def relPath(self, path):
        """Return the relative path from sandbox to given path
        """
        return os.path.relpath(path, self.dirname)
    
    def push(self, fname, targetFName = ""):
        if (targetFName == ""):
            targetFName = os.path.basename(fname)
        self.fs.copy(fname, os.path.join(self.dirname, targetFName))
        self.files.add(targetFName)
        
    def echoToFile(self, fname, contents):
        """Creates a new file with given contents
        """
        self.fs.echoToFile(os.path.join(self.dirname, fname), contents)
        self.files.add(fname)
        
    def exec(self, command,  args = "",  localRun = False):
        """localRun must be set to true if path to command is relative to current dir
        (this will force to use os.path.join(".", cmd) under Linux)"""
        pwd = os.path.abspath(self.fs.root())
        self.fs.chdir(self.dirname)
        self.fs.exec(command, args, localRun)
        self.fs.chdir(pwd)

    def pop(self, file, where):
        if os.path.isdir(where):
            where = os.path.join(where, os.path.basename(file))
        self.fs.copy(os.path.join(self.dirname, file), where)
        
    def newFiles(self):
        pwd = os.path.abspath(self.fs.root())
        self.fs.chdir(self.dirname)
        res = set(self.fs.files(".")) - self.files
        self.fs.chdir(pwd)
        return res
