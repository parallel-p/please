import os
import subprocess
import stat
import shutil
import unittest
from clone_repository import *

dirn = ["myfold_repo1", "myfold_repo2"]


class CloneRepository_test(unittest.TestCase):
    def tearDown(self):
        for dirname0 in dirn:
            for dirpath, dirnames, filenames \
                    in os.walk(dirname0, topdown=False):
                for filename in filenames:
                    filename = os.path.join(dirpath, filename)
                    os.chmod(filename, stat.S_IWRITE | stat.S_IREAD)
                    os.remove(filename)
                os.rmdir(dirpath)

    def test_clone(self):
        def addFiles():
            os.mkdir(dirn[0])
            f = open(os.path.join(dirn[0], ".gitignore"), "w")
            f.write("test")
            f.close()
            os.mkdir(os.path.join(dirn[0], "sub"))
            f = open(os.path.join(dirn[0], "sub", "abacaba"), "w")
            f.write("release")
            f.close()

        def gitCommand(folder, command_line):  # "folder" is subdirectory
            os.chdir(folder)
            try:
                out = subprocess.check_output(command_line)
            finally:
                os.chdir("..")
            return out

        addFiles()
        gitCommand(dirn[0], "git init")
        gitCommand(dirn[0], "git add .")
        gitCommand(dirn[0], "git commit -m 'Init'")
        clone_repository(dirn[0], dirn[1])

        out = [""] * 2
        command_line = "git ls-tree -r --name-only --full-tree master"
        for i, dirname in enumerate(dirn):
            out[i] = gitCommand(dirn[1], command_line)
        self.assertEqual(out[0], out[1])

    def test_dir_exists(self):
        for dirname in dirn:
            os.mkdir(dirname)
        with self.assertRaises(OSError):
            clone_repository(dirn[0], dirn[1])


if __name__ == '__main__':
    unittest.main()
