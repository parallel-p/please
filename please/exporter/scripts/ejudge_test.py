import please.exporter.scripts.ejudge as ejudge_exporter

import unittest, os

class CppTest(unittest.TestCase):
    def setUp(self):
        self.old_cwd = os.getcwd()

    def test_ejudge(self):
        cur_root = os.path.split(__file__)[0]
        os.chdir(os.path.join(cur_root, "tests", "please_tmp"))
        ejudge_exporter.export('../conf/serve.cfg', '../conf/serve.cfg.out')
        out = open('../conf/serve.cfg.out')
        corr = open('../conf/serve.cfg.corr')
        out_lines = out.readlines()
        corr_lines = corr.readlines()
        for x in range(len(out_lines)):
            self.assertEqual(out_lines[x], corr_lines[x])

    def tearDown(self):
        os.chdir(self.old_cwd)

if __name__ == '__main__':
    unittest.main()
