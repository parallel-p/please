import unittest
import users
import os


class TestUsers(unittest.TestCase):
    def test_register_user(self):
        group_exists = users.WEBPLEASE_GROUP in users.read_users('/etc/group')
        dir_exists = os.path.isdir(users.WEBPLEASE_PATH)
        username = 'iePei2iP'
        users.register_user(username, 'qwerty')
        if not group_exists:
            self.assertIn(users.WEBPLEASE_GROUP, users.read_users('/etc/group'))
        self.assertIn(username, users.read_users('/etc/passwd'))
        if not dir_exists:
            self.assertTrue(os.path.isdir(users.WEBPLEASE_PATH))
        self.assertTrue(os.path.isdir('/home/' + username))
        self.assertEqual(1000, os.stat(users.WEBPLEASE_PATH).st_mode & 1000)
        os.system('userdel ' + username)
        os.system('rm -r /home/' + username)
        if not dir_exists:
            os.system('rm -r ' + users.WEBPLEASE_PATH)
        if not group_exists:
            os.system('groupdel ' + users.WEBPLEASE_GROUP)

if __name__ == '__main__':
    unittest.main()
