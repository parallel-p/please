from please.template.source_code_file_generator import *
from os.path import exists
from os import mkdir, remove
from shutil import rmtree
import os

import unittest

class TestStatementDescriptionGenerator(unittest.TestCase):
    def setUp(self):
        if exists("t"):
            rmtree("t")
        mkdir("t")
        
    def tearDown(self):
        if exists("t"):
            rmtree("t")
        if exists("validator.cpp"):
            remove("validator.cpp")
        if exists("checker.cpp"):
            remove("checker.cpp")
        if exists("solution.cpp"):
            remove("solution.cpp")
    
    def test_validator_template1(self):
        generate_validator()
        self.assertTrue(exists("validator.cpp"))
        
    def test_validator_template2(self):
        generate_validator("t")
        self.assertTrue(exists(os.path.join("t", "validator.cpp")))

    def test_validator_template3(self):
        generate_validator("t", "py")
        self.assertTrue(exists(os.path.join("t", "validator.py")))
    
    
    def test_checker_template1(self):
        generate_checker()
        self.assertTrue(exists("checker.cpp"))
        
    def test_checker_template2(self):
        generate_checker("t")
        self.assertTrue(exists(os.path.join("t", "checker.cpp")))

    def test_checker_template3(self):
        generate_checker("t", "py")
        self.assertTrue(exists(os.path.join("t", "checker.py")))
    
    
    def test_solution_template1(self):
        generate_solution()
        self.assertTrue(exists("solution.cpp"))
        
    def test_solution_template2(self):
        generate_solution("t")
        self.assertTrue(exists(os.path.join("t", "solution.cpp")))

    def test_solution_template3(self):
        generate_solution("t", "py")
        self.assertTrue(exists(os.path.join("t", "solution.py")))
    
        
if __name__ == '__main__':
    unittest.main()
    
