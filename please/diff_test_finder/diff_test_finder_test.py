import unittest
import os
from .diff_test_finder import DiffTestFinder
from ..test_info.test_file import StrTestFile, FileTestFile

class TestDiffTestFinder(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_full_01(self):
        tmp = DiffTestFinder('*', '')
        tests, trash = tmp.tests('.', [[], []], 'stdout')
        self.assertEqual(tests[0].str, 'stdout')
        self.assertEqual(tests[1:], [])

    def test_full_02(self):
        tmp = DiffTestFinder('*', '')
        self.assertEqual(tmp.tests('.', [[], []])[0], [])

    def test_full_03(self):
        tmp = DiffTestFinder(os.path.join('..' , '*'), '*trash')
        tests = tmp.tests('gen', [[], ['01.in', 'trash', 'trash01', os.path.join('gen', '01.in')]])[0]
        correct = ['01.in', 'trash01']
        self.assertSetEqual(set(tests), set(correct))

    def test_full_04(self):
        tmp = DiffTestFinder(os.path.join('..', '*'), '*trash*')
        tests = tmp.tests('gen', [[], [os.path.join('gen', '01.in'), 'trash',
                                       os.path.join('..', 'trash01'),
                                       os.path.join('gen', '01.in')]])[0]
        correct = []
        self.assertSetEqual(set(tests), set(correct))

    def test_full_05(self):
        tmp = DiffTestFinder(os.path.join('..', '*'), '*trash*')
        tests = tmp.tests('gen', [[], [os.path.join('gen', '01.in'), 'trash',
                                       os.path.join('..', 'trash01'),
                                       os.path.join('gen', '01.in')]], 'stdout.out')[0]
        correct = ['stdout.out']
        self.assertSetEqual(set(tests), set(correct))
        
    
if __name__ == "__main__":
    unittest.main()
