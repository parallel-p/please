import unittest

from .file import File
from . import logging

class FileTest(unittest.TestCase):
    def test(self):
       for filename, extension, basename in [
               ("./ura.php", "php", "ura.php"),
               ("././dere/.svn/ura.cpp", "cpp", "ura.cpp"),
               ("ewr/ura", "", "ura")]:
           f = File(filename)
           self.assertEqual(f.extension(), extension)
           self.assertEqual(f.basename(), basename)


class ConsoleLogTest(unittest.TestCase):
    def setUp(self):
        self.log = logging.ConsoleLog()

    def test_colors(self):
        self.log.debug('this is debug')
        self.log.info('this is info')
        self.log.notice('this is notice')
        self.log.warning('this is warning')
        self.log.error('this is error')
        self.log.fatal('this is fatal')
        self.log.log(logging.NO_LOGGING, 'no logging now')
        self.log.info('this is info')


if __name__ == '__main__':
    unittest.main()
