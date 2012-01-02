import unittest
import os
from please.language.language import Language
from please.language import program_detector

class TestLanguageDetection(unittest.TestCase):
    
    def test_is_program_detect(self):
        self.assertTrue(program_detector.is_program_detect("C://somefolder.olo//program.test.cpp"))
        self.assertTrue(program_detector.is_program_detect("C://somefolder.olo//program.test.c++"))
        self.assertTrue(program_detector.is_program_detect("C://somefolder.olo//program.tester.dpr"))
        self.assertTrue(program_detector.is_program_detect("C://somefolder.olo//program.test.cs"))
        self.assertTrue(program_detector.is_program_detect("C://somefolder.tests//program.test.java"))
        self.assertTrue(program_detector.is_program_detect("C://somefolder.olo//program.test.py"))
        self.assertTrue(program_detector.is_program_detect("C://somefolder.olo//program.test.dpr"))
        self.assertFalse(program_detector.is_program_detect("C://somefolder.olo//NotProgram.test"))
        self.assertFalse(program_detector.is_program_detect("C://somefolder.tests//NotProgram"))
        self.assertFalse(program_detector.is_program_detect("C://somefolder.tests//NotProgram"))
        
if __name__ == "__main__":
    unittest.main()
