import unittest
from .diff_test_finder import DiffTestFinder

class TestDiffTestFinder(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_full_01(self):
        tmp = DiffTestFinder('.', '.*', '')
        self.assertEqual(tmp.tests([[], []], 'stdout.out'), ['stdout.out'])

    def test_full_02(self):
        tmp = DiffTestFinder('.', '.*', '')
        self.assertEqual(tmp.tests([[], []]), [])

    def test_full_03(self):
        tmp = DiffTestFinder('gen', '\\.\\./.*', '.*trash$')
        tests = tmp.tests([[], ['01.in', 'trash', 'trash01', 'gen/01.in']])
        correct = ['../01.in', '../trash01']
        self.assertSetEqual(set(tests), set(correct))

    def test_full_04(self):
        tmp = DiffTestFinder('gen', '\\.\\./\w*$', '.*trash$')
        tests = tmp.tests([[], ['gen/01.in', 'trash', '../trash01', 'gen/01.in']])
        correct = []
        self.assertSetEqual(set(tests), set(correct))

    def test_full_05(self):
        tmp = DiffTestFinder('gen', '\\.\\./\w*$', '.*trash$')
        tests = tmp.tests([[], ['gen/01.in', 'trash', '../trash01', 'gen/01.in']], 'stdout.out')
        correct = ['stdout.out']
        self.assertSetEqual(set(tests), set(correct))
        
    
if __name__ == "__main__":
    unittest.main()