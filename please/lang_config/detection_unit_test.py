import unittest
import os

from please.lang_config import get_language
from please.utils.exceptions import PleaseException
class TestLanguageDetection(unittest.TestCase):
    
    def __basename(self, str):
        pos = str.rfind(".")
        if (pos == -1):
            return str
        else:
            return str[:pos]
    
    def test_on_test_files(self):
        root = os.path.join(os.path.dirname(__file__), 'detection_test_files')
        for file in os.listdir(root):
            if not os.path.isfile(os.path.join(root, file)):
               continue
            ansfile = file + ".ans"
            if not os.path.isfile(os.path.join(root, ansfile)):
                continue
            with open(os.path.join(root, ansfile), "r") as f:
                ans = f.readline().strip()
                result = get_language(os.path.join(root, file))
                if (ans != "undefined"):
                    self.assertEqual(ans, result, file + " was not determined correctly\n")
                else:
                    self.assertIsNone(result, file + " was not determined correctly\n")

    @unittest.skip("actually, this is delayed to config creation")
    def test_non_exist(self):
        with self.assertRaises(PleaseException):
            get_language("random.py")
        
if __name__ == "__main__":
    unittest.main()
