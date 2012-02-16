from please.commands.template import Template
import unittest
from os.path import join as _j

class TemplateTest(unittest.TestCase):
    def _test(self, template, args, **dict):
        t = Template(template)
        args = args.split()
        self.assertEqual(t.match(args, 'tmp'), dict)

    def test_correct(self):

        self._test("add tag $tag", "add tag a", tag = "a")
        self._test("add tag tag...", "add tag a b c", tag = "a b c".split())
        self._test("[add] tag $tag", "add tag a", tag = "a")
        self._test("[ add ] tag $tag", "tag a", tag = "a")

        self._test("svn praise|blame /path",
                   "svn praise a.py",
                   path = _j("tmp", "a.py"))

        self._test("svn praise|blame /path",
                   "svn blame a.py",
                   path = _j("tmp", "a.py"))

        self._test("add tag[s] tags... to file /project",
                   "add tags a b c to file helloworld.py",
                   tags = "a b c".split(),
                   project = _j("tmp", "helloworld.py"))
        self._test("generate with /file tests...",
                   "generate with generator.py test1 test2 test3",
                   file = _j("tmp", "generator.py"),
                   tests = "test1 test2 test3".split())

if __name__ == "__main__":
    unittest.main()

