import unittest
import os

from please.language.language import Language

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
        #print(os.listdir(root))
        for file in os.listdir(root):
            #print(file)
            if not os.path.isfile(root + file):
                continue
            ansfile = file + ".ans"
            if not os.path.isfile(root + ansfile):
                continue
            
            with open(root + ansfile, "r") as f:
                ans = f.readline()    
                result = lang.get(root + file)
                #print(result)
                #print(ans)
                if (ans != "undefined"):
                    self.assertEqual(ans,result, file + " was not determined correctly\n")
                else:
                    self.assertIsNone(result, file + " was not determined correctly\n")
                    
    def test_non_exist(self):
        lang = Language()
        f = False
        try:
            lang.get("random.py")
        except OSError:
            f = True
        self.assertTrue(f)
        
if __name__ == "__main__":
    unittest.main()
