import unittest
from  please.command_line.matcher import Matcher

class MatcherTest(unittest.TestCase):

    def test_matches(self):
        clm = Matcher()
        clm.add_handler(NoneTemplate(), lambda: self.return_0(), True)
        clm.add_handler(ConstTemplate(), lambda a, b: self.const_call(a, b), True)
        self.assertEqual(clm.matches("ASDASD"), "const_call")

    def test_matches_throws_exceptions_no_match(self):
        clm = Matcher()
        clm.add_handler(NoneTemplate(), lambda: self.return_0(), True)
        self.assertRaises(Exception, clm.matches, "ASD")
        self.assertRaises(Exception, clm.matches, "QWE")

    def test_matches_throws_exceptions_two_match(self):
        clm = Matcher()
        clm.add_handler(ConstTemplate(), lambda a, b: self.const_call(a, b), True)
        clm.add_handler(ConstTemplate(), lambda a, b: self.const_call(a, b), True)
        self.assertRaises(Exception, clm.matches, "ASD")

    def return_0(self):
        self.assertTrue(False)
        return 0

    def const_call(self, a, b):
        self.assertEqual(a, [1, 2, 3])
        self.assertEqual(b, "123")
        return "const_call"

class ExceptionTemplate:
    def corresponds(self, startdir, args):
        return

class NoneTemplate:
    def corresponds(self, startdir, args):
        return None;

class ConstTemplate:
    def corresponds(self, startdir, args):
        return {"a" : [1,2,3], "b" : "123"};

if __name__ == "__main__":
    unittest.main()

