import unittest
from . import cmd_gen_test_info
import os
import shutil

class CmdOrGenTestInfo(unittest.TestCase):
    
    def test_generator(self):
        stdir = os.getcwd()
        a = cmd_gen_test_info.CmdOrGenTestInfo("test_problems/generator/main.cpp", ["blue", "dog"])
        res = a.tests()
        
        self.assertEqual(res[0].contents(), "blue dog ")
        
if __name__ == '__main__':
    unittest.main()
