from please.commands.template import Template
import unittest
from os.path import join as _j

class TemplateTest(unittest.TestCase):
    def _test(self, template, args, **dict):
        t = Template(template)
        args = args.split()
        self.assertEqual(t.match(args), dict)

    def test_correct(self):
        # Simple cases
        self._test("add tag $tag", "add tag a", tag = "a")
        self._test("add tag tag...", "add tag a b c", tag = "a b c".split())
        self._test("[add] tag $tag", "add tag a", tag = "a")
        self._test("[ add ] tag $tag", "tag a", tag = "a")

        # Or-clause.
        self._test("svn praise|blame /path",
                   "svn praise a.py",
                   path = "a.py")

        self._test("svn praise|blame /path",
                   "svn blame a.py",
                   path = "a.py")

        self._test("add tag[s] tags... to file /project",
                   "add tags a b c to file helloworld.py",
                   tags = "a b c".split(),
                   project = "helloworld.py")

        # Arg - list
        self._test("generate with /file tests...",
                   "generate with generator.py test1 test2 test3",
                   file = "generator.py",
                   tests = "test1 test2 test3".split())

        # List - arg
        self._test("merge-into files... /file",
                   "merge-into variant.1 variant.2 variant.3 everything",
                   files = 'variant.1 variant.2 variant.3'.split(),
                   file = 'everything')

        # Mistakes
        self._test("please make me sandwich", "please make me sandwitch")
        self._test("svn blame /file", "svm blam test.py", file = 'test.py')
        self._test("ls files...", "ld file1 file2 file3",
                   files = 'file1 file2 file3'.split())

    def _test_unmatch(self, template, args):
        m, r = Template(template).match_ratio(args.split())
        self.assertEqual(m, None, r)

    def test_incorrect(self):
        self._test_unmatch("and now for", "something completely different")
        self._test_unmatch("add [tag] $tag", "tag tag1")

if __name__ == "__main__":
    unittest.main()

