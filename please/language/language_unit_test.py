import unittest
import os

from please.language.language import Language
from please.utils.exceptions import PleaseException
class TestLanguageDetection(unittest.TestCase):
    
    def __basename(self, str):
        pos = str.rfind(".")
        if (pos == -1):
            return str
        else:
            return str[:pos]
    
    def test_on_test_files(self):
        root = os.path.join(".", "please", "language", "test_files")
        lang = Language()
        for file in os.listdir(root):
            if not os.path.isfile(os.path.join(root, file)):
               continue
            ansfile = file + ".ans"
            if not os.path.isfile(os.path.join(root, ansfile)):
                continue
            
            with open(os.path.join(root, ansfile), "r") as f:
                ans = f.readline()    
                result = lang.get(os.path.join(root, file))
                if (ans != "undefined"):
                    self.assertEqual(ans, result, file + " was not determined correctly\n")
                else:
                    self.assertIsNone(result, file + " was not determined correctly\n")
                    
    def test_non_exist(self):
        lang = Language()
        f = False
        try:
            lang.get("random.py")
        except PleaseException:
            f = True
        self.assertTrue(f)
        
if __name__ == "__main__":
    unittest.main()
