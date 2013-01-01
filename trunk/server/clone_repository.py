import os
import brigit


def clone_repository(source, destination):
    if os.path.exists(destination):
        raise OSError()
    brigit.Git(os.path.join(os.curdir, destination), remote=source)
