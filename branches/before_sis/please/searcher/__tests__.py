import unittest
from mock import Mock
from checker import Checker

class CheckerTest(unittest.TestCase):

    def test_check_exists_checker(self):
        import os.path
        for just_file in [os.path.join(dir, name + "." + ext)
                for dir in [".", "", "sources"]
                for name in ["check", "checker", "check_default"]
                for ext in ["cpp", "py", "pas", "dpr"]]:
            fs = Mock()
            fs.find = Mock(return_value = [just_file])
            self.assertEqual(Checker(fs).file(), just_file)

    def test_check_not_exists_checker(self):
        for found_files in [
                ["check.cpp", "checker.pas"],
                [],
                ["a", "b", "c"]]:
            fs = Mock()
            fs.find = Mock(return_value = found_files)
            self.assertEqual(Checker(fs).file(), None)

if __name__ == '__main__':
    unittest.main()
