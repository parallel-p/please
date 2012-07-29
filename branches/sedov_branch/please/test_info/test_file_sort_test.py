import unittest
from . import test_file_sort 
from .test_file import FileTestFile

class TestFileSort(unittest.TestCase):
        
    def test_sorting_key(self):
        for word in ["hello", "hello.in", "hello.out", "xyz.abc.zyx"]:
            self.assertEqual(test_file_sort.sorting_key(word), (word,))
        for number in ["123", "0154", "01", "1"]:
            self.assertEqual(test_file_sort.sorting_key(number), (int(number),))
        self.assertEqual(test_file_sort.sorting_key("1" + "0" * 100), (10**100,))
        for word, number in [("abc", "123"), ("a", "0154"), ("qw", "01"), (".", "1")]:
            self.assertEqual(test_file_sort.sorting_key(word + number),
                    (word, int(number)))
            self.assertEqual(test_file_sort.sorting_key(number + word),
                    (int(number), word))
        self.assertEqual(test_file_sort.sorting_key("bank.10.in"),
                ("bank.", 10, ".in"))
        self.assertEqual(test_file_sort.sorting_key("12.bank.10.in.11"),
                (12, ".bank.", 10, ".in.", 11))
        self.assertEqual(test_file_sort.sorting_key("bank.10.in.11"),
                ("bank.", 10, ".in.", 11))
        self.assertEqual(test_file_sort.sorting_key("12.bank.10.in"),
                (12, ".bank.", 10, ".in"))
        
if __name__ == '__main__':
    unittest.main()

