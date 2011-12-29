.import unittest
.import mox
.from . import file_test_info
.import os
.
.class FileTestInfoTest(unittest.TestCase):
.    def setUp(self):
.        self.mox = mox.Mox()
.        
.    def tearDown(self):
.        self.mox.UnsetStubs()
.        self.mox.VerifyAll()
.        
.    def test_one_big(self):
.        myfilename = "my.txt"
.        
.        pig = open(myfilename , "w")
.        pig.write("test")
.        pig.close()
.        
.        fti = file_test_info.FileTestInfo("my.txt", {"to":"be", "or":"not"})
.        r = fti.tests()
.        
.        self.assertEqual(fti.get_tags(), {"to":"be", "or":"not"})
.        strres = fti.to_please_format()
.        self.assertEqual(strres, "[or = not, to = be] my.txt")
.        
.        newfile = open(r[0], "r")
.        self.assertEqual(newfile.read(), "test")
.        newfile.close()
.        
.        os.remove(r[0])
.        os.remove(myfilename)
.        
.if __name__ == '__main__':
.    unittest.main()