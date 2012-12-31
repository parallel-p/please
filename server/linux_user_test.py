import unittest
import linux_user
import os


class TestUsers(unittest.TestCase):
    def test_register_user(self):
        group_exists = linux_user.WEBPLEASE_GROUP in linux_user.read_users('/etc/group')
        dir_exists = os.path.isdir(linux_user.WEBPLEASE_PATH)
        username = 'iePei2iP'
        linux_user.register_user(username)
        if not group_exists:
            self.assertIn(linux_user.WEBPLEASE_GROUP, linux_user.read_users('/etc/group'))
        self.assertIn(username, linux_user.read_users('/etc/passwd'))
        if not dir_exists:
            self.assertTrue(os.path.isdir(linux_user.WEBPLEASE_PATH))
        self.assertTrue(os.path.isdir('/home/' + username))
        self.assertEqual(1000, os.stat(linux_user.WEBPLEASE_PATH).st_mode & 1000)
        os.system('userdel ' + username)
        os.system('rm -r /home/' + username)
        if not dir_exists:
            os.system('rm -r ' + linux_user.WEBPLEASE_PATH)
        if not group_exists:
            os.system('groupdel ' + linux_user.WEBPLEASE_GROUP)

if __name__ == '__main__':
    unittest.main()
