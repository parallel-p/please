import os
import subprocess
import stat
import shutil
import unittest
from create_repository import *


class CreateRepositoryFromDir_test(unittest.TestCase):
    def test_create(self):
        def addFiles():
            os.mkdir(dirn[0])
            os.chdir(dirn[0])
            f = open(".gitignore", "w")
            f.write("test")
            f.close()
            os.mkdir("sub")
            os.chdir("sub")
            f = open("abacaba", "w")
            f.write("release")
            f.close()

        dirn = ["myfold", "myfold_repo"]
        startdir = os.getcwd()
        try:
            addFiles()
            os.chdir(startdir)
            create_repository_from_dir(dirn[0], dirn[1],
                                       User("Username", "mail"))
            os.chdir(startdir)
            os.chdir(dirn[1])
            command_line = "git ls-tree -r --name-only --full-tree master"
            out = subprocess.check_output(command_line)
            self.assertEqual(out.decode("ASCII").split("\n")[:-1],
                             [".gitignore", "sub/abacaba"])
        finally:
            os.chdir(startdir)
            for dirname0 in dirn:
                for dirpath, dirnames, filenames \
                        in os.walk(dirname0, topdown=False):
                    for filename in filenames:
                        filename = os.path.join(dirpath, filename)
                        os.chmod(filename, stat.S_IWRITE | stat.S_IREAD)
                        os.remove(filename)
                    os.rmdir(dirpath)

if __name__ == '__main__':
    unittest.main()
