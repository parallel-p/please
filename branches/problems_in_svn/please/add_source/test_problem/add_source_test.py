import unittest
import os
from please.add_source.add_source import add_solution
from please.add_source.add_source import add_checker
from please.add_source.add_source import add_validator

class AddSourceTest (unittest.TestCase):
    def setUp(self):
        self.rdir = os.getcwd()
        root = os.path.split(__file__)[0]
        os.chdir(root)
        
    def tearDown(self):
        open("default.package","w").write("")
        os.chdir(self.rdir)
        
    def test_add_solution(self):

        path = "testdata/sol.cpp"
        expected_list = ["OK"]
        possible_list = ["TL","ML","RE"]
        add_solution(path,expected_list,possible_list)
        self.assertTrue(os.path.exists(os.path.join("solutions","sol.cpp")))

    def test_add_checker(self):
        path = "testdata/check_code.cpp"
        add_checker(path)
        self.assertTrue(os.path.exists(os.path.join("check_code.cpp")))

    def test_add_validator(self):
        path = "testdata/validate_tests.cpp"
        add_validator(path)
        self.assertTrue(os.path.exists(os.path.join("validate_tests.cpp")))



if __name__ == '__main__':
    unittest.main()     