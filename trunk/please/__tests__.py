import unittest
from file import File

class FileTest(unittest.TestCase):
    def test(self):
       for filename, extension, basename in [
               ("./ura.php", "php", "ura.php"),
               ("././dere/.svn/ura.cpp", "cpp", "ura.cpp"),
               ("ewr/ura", "", "ura")]:
           f = File(filename)
           self.assertEqual(f.extension(), extension)
           self.assertEqual(f.basename(), basename)

if __name__ == '__main__':
    unittest.main()
