import unittest
from . import cmd_gen_test_info
import os
import shutil

class CmdOrGenTestInfo(unittest.TestCase):
    
    def test_generator(self):
        stdir = os.getcwd()
        a = cmd_gen_test_info.CmdOrGenTestInfo("test_problems/generator/main.cpp", ["blue", "dog"])
        res = a.tests()
        
        #TODO:what is res[0]?
        with open(res[0]) as res_file:
            self.assertEqual(res_file.read(), "blue dog ")
        os.remove(res[0])
        
if __name__ == '__main__':
    unittest.main()
