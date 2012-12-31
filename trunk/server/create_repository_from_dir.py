import pygit2
import shutil
import glob
import os
import re


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email


def create_repository_from_dir(source, destination, user):
    shutil.copytree(source, destination)
    repo = pygit2.init_repository(destination, False)
    author = pygit2.Signature(user.name, user.email)
    committer = pygit2.Signature('webserver', 'admin@webserver')
    os.chdir(destination)
    for dirpath, dirnames, filenames in os.walk('.'):
        if dirpath == '.':
            dirnames.remove(".git")
        for filename in filenames:
            repo.index.add(os.path.join(dirpath, filename).
                           replace("\\", "/")[2:])
    repo.index.write()
    tree = repo.index.write_tree()
    repo.create_commit('refs/heads/master', author, committer,
                       'Init commit', tree, [])
