#!/usr/bin/python

from . import file
from .. import sandbox
import os.path

class Generator(object):
    """Interprets a given generate.please file."""
    
    def __init__(self, filename, log,  locale,  config):
        self.file = file.File(filename)
        self.log = log
        self.locale = locale
        self.config = config
        
    def execute(self, outputDir):
        nTests = 0
        for cmd in self.file.script:
            cmd = cmd.rstrip(" \n\r")
            self.log.info(self.locale.get('generator.running-command').format(cmd))
            hint = os.path.splitext(os.path.basename(cmd))[0]
            sb = sandbox.Sandbox(hint)
            
            sb.push(os.path.join(self.config.testsDir(), cmd))
            sb.exec(cmd, "", True)
            nf = sb.newFiles()
            tests = {}
            for file in nf:
                if (os.path.splitext(file)[1] != ".a"):
                    inf = file
                    if file + ".a" in nf: ouf = file +".a"
                    else: ouf = None
                    tests[inf] = ouf
            for inf in sorted(tests.keys()):
                nTests += 1
                targetFile = self.config.inputFormat() % nTests
                self.log.debug(self.locale.get('generator.test-found') 
                               % (nTests, inf, targetFile))
                sb.pop(inf, os.path.join(outputDir, targetFile))
                if tests[inf]:
                    targetFile = self.config.answerFormat() % nTests
                    self.log.debug(self.locale.get('generator.answer-found') 
                                   % (tests[inf], targetFile))
                    sb.pop(tests[inf], os.path.join(outputDir, targetFile))
            
    
