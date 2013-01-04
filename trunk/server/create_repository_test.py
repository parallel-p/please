import os
import subprocess
import stat
import shutil
import unittest
from create_repository import *

dirn = ["myfold", "myfold_repo"]


class CreateRepositoryFromDir_test(unittest.TestCase):
    def tearDown(self):
        for dirname0 in dirn:
            for dirpath, dirnames, filenames \
                    in os.walk(dirname0, topdown=False):
                for filename in filenames:
                    filename = os.path.join(dirpath, filename)
                    os.chmod(filename, stat.S_IWRITE | stat.S_IREAD)
                    os.remove(filename)
                os.rmdir(dirpath)

    def test_create(self):
        def addFiles():
            os.mkdir(dirn[0])
            f = open(os.path.join(dirn[0], ".gitignore"), "w")
            f.write("test")
            f.close()
            os.mkdir(os.path.join(dirn[0], "sub"))
            f = open(os.path.join(dirn[0], "sub", "abacaba"), "w")
            f.write("release")
            f.close()

        addFiles()
        create_repository_from_dir(dirn[0], dirn[1],
                                   User("Username", "mail"))
        os.chdir(dirn[1])
        command_line = "git ls-tree -r --name-only --full-tree master"
        try:
            out = subprocess.check_output(command_line)
        finally:
            os.chdir("..")
        self.assertListEqual(sorted(out.decode("ASCII").split("\n")[:-1]),
                             sorted([".gitignore", "sub/abacaba"]))

if __name__ == '__main__':
    unittest.main()
