from please.commands.matcher import Matcher
import unittest
import mox

class MatcherTest(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_exact_match(self):
        obj = self.mox.CreateMockAnything()
        m = Matcher()
        obj.add(file="test_add")
        obj.mv(file1="test_mv1", file2="test_mv2")
        obj.rm(file="test_rm")
        self.mox.ReplayAll()
        m.add("rm /file", obj.rm)
        m.add("add /file", obj.add)
        m.add("mv /file1 /file2", obj.mv)
        match = lambda s: m.match(s.split())
        self.assertTrue(match("add test_add"))
        #path normalization
        self.assertTrue(match("mv dir1/dir2/../../test_mv1 ./test_mv2"))
        self.assertTrue(match("rm test_rm"))
        self.assertFalse(match("info"))
        self.mox.VerifyAll()

    def test_preference(self):
        obj = self.mox.CreateMockAnything()
        m = Matcher()
        obj.ls(files = ['dir'])
        obj.ls(files = ['path1', 'path2', 'path3'])
        obj.ld(files = ['path1', 'path2', 'path3'])
        obj.install(packages = ['python-please'])
        obj.install(packages = ['python3.2'])
        self.mox.ReplayAll()
        m.add("ls files...", obj.ls)
        m.add("install packages...", obj.install)

        match = lambda s: m.match(s.split())
        self.assertTrue(match("ls dir"))
        self.assertTrue(match("ld path1 path2 path3")) # here mistake in ls

        m.add("ld files...", obj.ld)
        self.assertTrue(match("ld path1 path2 path3")) # and here is command

        self.assertTrue(match("isnall python-please"))
        self.assertTrue(match("instlal python3.2"))

        self.mox.VerifyAll()

if __name__ == '__main__':
    unittest.main()
