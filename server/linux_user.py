import os
import shutil
import random
import string
import crypt
import stat


WEBPLEASE_PATH = '/opt/webplease'
WEBPLEASE_GROUP = 'webplease'
WEBPLEASE_OWNER = 'root'


def pwgen(count):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(count))


class GroupError(Exception):
    pass


class UserError(Exception):
    pass


def read_users(filename):
    with open(filename) as file:
        users = [line.split(':')[0] for line in file]
    return users


def add_group():
    if WEBPLEASE_GROUP not in read_users('/etc/group'):
        exitcode = os.system('groupadd ' + WEBPLEASE_GROUP)
        if exitcode:
            raise GroupError('Exit code: ' + str(exitcode))


def add_directory():
    add_group()
    if not os.path.isdir(WEBPLEASE_PATH):
        os.mkdir(WEBPLEASE_PATH)
        shutil.chown(WEBPLEASE_PATH, user=WEBPLEASE_OWNER, group=WEBPLEASE_GROUP)
        os.chmod(WEBPLEASE_PATH, mode=(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_ISVTX))


def set_password(username, password):
    if username in read_users('/etc/passwd'):
        salt = pwgen(8)
        hashed_password = crypt.crypt(password, salt)
        exitcode = os.system('usermod -p {} {}'.format(hashed_password,
                                                       username))
        if exitcode:
            raise UserError('Can not change password - exit code: ' + str(exitcode))


def register_user(username):
    add_directory()
    if username not in read_users('/etc/passwd'):
        exitcode = os.system('useradd -m -g users -G {} -s /bin/bash {}'.format(WEBPLEASE_GROUP,
                                                                                username))
        if exitcode:
            raise UserError('Exit code: ' + str(exitcode))

if __name__ == '__main__':
    register_user(input('Enter username: '))
