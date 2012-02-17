import unittest
import mox
import os.path

from please import stress_tester
from please.package import package_config
from please.utils.exceptions import PleaseException
#import please

class FakeInvokerReport():
    verdict = "OK"
    return_code = 0

class TestStressTester(unittest.TestCase):
    class FakeFile():
        def __init__(self):
            pass

        def __exit__(self, arg1, arg2, arg3):
            pass

        def __enter__(self):
            pass

        def read(self):
            return "ansdata"

        def write(self, data):
            pass

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()
        
    def test_integration(self):
        current_dir = os.getcwd()
        try:
            cur_root = os.path.split(__file__)[0]
            os.chdir(os.path.join(cur_root, "test_problem"))
            tester = stress_tester.StressTester(
                package_config.PackageConfig.get_config(ignore_cache = True))
            print(os.path.exists(os.path.join('tests', 'generator.cpp')))
            tester(os.path.join('tests', 'generator.cpp'),
                   os.path.join('solutions', 'solution_wrong.cpp'),
                   os.path.join('solutions', 'solution.cpp'))
        except PleaseException as ex:
            print(ex)
        finally:
            os.chdir(current_dir)
        self.assertRaises(stress_tester.StressCheckMatchException)
        self.assertRaises(PleaseException)

if __name__ == "__main__":
    unittest.main()
