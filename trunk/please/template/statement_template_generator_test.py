from please.template.statement_template_generator import *
from os.path import exists
from os import mkdir, remove
from shutil import rmtree
import os

import unittest

class TestStatementDescriptionGenerator(unittest.TestCase):
    def setUpClass():
        if not os.path.exists("test"):
           mkdir("test")
        
    def tearDownClass():
        if exists("test"):
            rmtree("test")
        if exists("default.tex"):
            remove("default.tex")
        if exists("description.tex"):
            remove("description.tex")
    
    def test_statement1(self):
        generate_statement()
        self.assertTrue(exists("default.tex"))
        
    def test_statement2(self):
        generate_statement("test")
        self.assertTrue(exists("test/default.tex"))

    def test_statement3(self):
        generate_statement("test", "rus", "hard")
        self.assertTrue(exists("test/hard.rus.tex"))
        
    def test_statement4(self):
        generate_statement("test", "eng")
        self.assertTrue(exists("test/default.eng.tex"))
        
    def test_description1(self):
        generate_description()
        self.assertTrue(exists("description.tex"))
        
    def test_description2(self):
        generate_description("test", "ukr", "easy")
        self.assertTrue(exists("test/easy.ukr.tex"))
        
    def test_description3(self):
        generate_description("test")
        self.assertTrue(exists("test/description.tex"))
        
    def test_description4(self):
        generate_description("test", "rus")
        self.assertTrue(exists("test/description.rus.tex"))
        
if __name__ == '__main__':
    unittest.main()
