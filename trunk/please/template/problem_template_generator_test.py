from os.path import exists
from os import mkdir, remove
from shutil import rmtree, copytree
import os
import unittest

from please.template.problem_template_generator import *
from please.svn import delete_problem

class TestStatementDescriptionGenerator(unittest.TestCase):
    def setUpClass():
        pass
    
    def tearDownClass():
        if exists("aplusb"):
            delete_problem("aplusb")
        if exists("cats"):
            shutil.rmtree("cats")
        
    def test_problem1(self):
        generate_problem('aplusb')
        for x in ['default.package', 
                  os.path.join('statements', 'default.ru.tex'), 
                  'tests', 
                  'checker.cpp', 
                  os.path.join('solutions', 'solution.cpp'), 
                  os.path.join('statements', 'description.ru.tex')]:
            self.assertTrue(exists(os.path.join("aplusb", x)), "There is no " + x)
          
    def test_problem2(self):
        generate_problem_advanced('cats', 'en', 'pas')
        for x in ['default.package', 
                  os.path.join('statements', 'default.en.tex'), 
                  'tests', 
                  'checker.pas', 
                  os.path.join('solutions', 'solution.pas'), 
                  os.path.join('statements', 'description.en.tex')]:
            self.assertTrue(exists(os.path.join("cats", x)), "There is no " + x)
        
if __name__ == '__main__':
    unittest.main()
