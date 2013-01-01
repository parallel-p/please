import pygit2
import shutil
import os


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email


def rel_posix_path(destination, dirpath, filename):
    # change directory separator to posix '/'
    # else in Windows git incorrectly adds files
    return '/'.join(
        os.path.relpath(  # path from the root of git repo
           os.path.join(dirpath, filename), destination
        ).split(os.sep)
    )


def create_repository_from_dir(source, destination, user):
    shutil.copytree(source, destination)
    repo = pygit2.init_repository(destination, False)
    author = pygit2.Signature(user.name, user.email)
    committer = pygit2.Signature('webserver', 'admin@webserver')
    for dirpath, dirnames, filenames in os.walk(destination):
        if dirpath == destination:  # don't add to repo ".git" directory
            dirnames.remove(".git")
        for filename in filenames:
            repo.index.add(rel_posix_path(destination, dirpath, filename))
    repo.index.write()
    tree = repo.index.write_tree()
    repo.create_commit('refs/heads/master', author, committer,
                       'Init commit', tree, [])
