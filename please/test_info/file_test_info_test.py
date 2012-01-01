import unittest
from . import file_test_info
import os

class FileTestInfoTest(unittest.TestCase):
        
    class WellDoneMock():
        def __init__(self, check_functions_list):
            self.__check_functions_list = check_functions_list
        def check(self, filename):
            return True
    
    def test_one_big(self):
        well_done = self.WellDoneMock(['no_symbols_less_32', 'no_left_right_space'])
        myfilename = "my.txt"
        
        with open(myfilename , "w") as pig:
            pig.write("test")
        
        fti = file_test_info.FileTestInfo("my.txt", {"to":"be", "or":"not"}, well_done)
        r = fti.tests()
        
        self.assertDictEqual(fti.get_tags(), {"to":"be", "or":"not"})
        strres = fti.to_please_format()
        self.assertEqual(strres, "[or = not, to = be] my.txt")
        
        with open(r[0], "r") as newfile:
            self.assertEqual(newfile.read(), "test")
        
        os.remove(r[0])
        os.remove(myfilename)
        
if __name__ == '__main__':
    unittest.main()
