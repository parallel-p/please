import unittest
import sys
from coverage import coverage
from please import log

def analysis(infile):
     strings = infile.read().split("\n")
     errors = []
     count = 0
     for s in strings:
          if ("ERROR" in s or "FAIL" in s) and len (s) > 5 :
               errors.append(s)
               count += 1
          if "==" in s:
               break     
     print("")
     if count == 0 :
          print(" Result = OK")
     else:
          print("Errors and fails:")
          print("")
          for error in errors:
               print(error)
          print("")
          print ("FAILS = " + str(count))
          print("")
          print ("Details in file test.log")


def run_tests(directory):
     print("Adding tests")
     suite.addTests(loader.discover(directory,"*_test.py"))
     print("Start testing")
     outfile =  open ("test.log", "w")
     infile = open ("test.log", "r")
     unittest.TextTestRunner(stream = outfile, verbosity = 100).run(suite)
     outfile.close()
     print("Testing finished")
     analysis(infile)

     
def run_consol_test(directory):
     suite.addTests(loader.discover(directory,"*_test.py"))
     unittest.TextTestRunner(verbosity = 2).run(suite)


args = sys.argv
loader = unittest.TestLoader()
suite = unittest.TestSuite()

if len(args) < 3 or args[2] != "coverage":
	cov = coverage(config_file=True)
	cov.start()

if len(args) == 1 :
     run_consol_test (".")
     

if len(args) == 2:
     if args[1] == "short":
          run_tests(".")
     else:
          run_consol_test(args[1])

if len(args) == 3:
     if args[2] == "short":
          run_tests(args[1])
     else:
          run_consol_test(".")
if len(args) < 3 or args[2] != "coverage":
	cov.stop()
	cov.html_report()
