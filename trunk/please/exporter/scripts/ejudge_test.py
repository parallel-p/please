import please.exporter.scripts.ejudge as ejudge_exporter
import please.exporter.scripts.ejudge_formatter as ejudge_formatter

import unittest, os, mox

class FakeFormatter():
    def __init__(self):
        pass
    def put_all(self):
        pass

class CppTest(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.old_cwd = os.getcwd()

    def test_ejudge(self):
        self.mox.StubOutWithMock(ejudge_formatter, 'EjudgeFormatter')
        self.mox.StubOutWithMock(ejudge_formatter, 'NewEjudgeFormatter')
        ejudge_formatter.EjudgeFormatter(mox.IgnoreArg()).AndReturn(FakeFormatter())
        ejudge_formatter.NewEjudgeFormatter(mox.IgnoreArg()).AndReturn(FakeFormatter())
        self.mox.ReplayAll()

        cur_root = os.path.split(__file__)[0]
        os.chdir(os.path.join(cur_root, "tests", "please_tmp"))
        ejudge_exporter.export('../conf/serve.cfg', '../conf/serve.cfg.out')
        with open('../conf/serve.cfg.out') as output:
            out_lines = output.readlines()
        with open('../conf/serve.cfg.corr') as correct:
            corr_lines = correct.readlines()
        for checked, answer in zip(out_lines, corr_line):
            self.assertEqual(checked, answer)

    def tearDown(self):
        self.mox.UnsetStubs()
        os.chdir(self.old_cwd)

if __name__ == '__main__':
    unittest.main()
