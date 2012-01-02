import unittest
import os.path
import os
import shutil
from please.template.template_utils import *
from please.globalconfig import root

class TestStatementDescriptionGenerator(unittest.TestCase):
    def setUpClass():
        if not os.path.exists("testdata"):
            os.mkdir("testdata")
        
    def tearDownClass():
        if os.path.exists("testdata"):
            shutil.rmtree("testdata")
            
    def test_copy_or_create(self):
        copy_or_create("testdata/abacaba.t", "testdata/ololo.t")
        self.assertTrue(os.path.exists("testdata/ololo.t"))
        
    def test_get_template_full_path(self):
        path = get_template_full_path("statement.tex")
        self.assertEqual(os.path.join(root, "templates", "statement.tex"), path)
        
if __name__ == "__main__":
    unittest.main()
