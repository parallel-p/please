import unittest
import sys



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
     return(count)

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
     return len(unittest.TextTestRunner(verbosity = 2).run(suite).errors)

args = sys.argv
loader = unittest.TestLoader()
suite = unittest.TestSuite()

run = run_consol_test
if len(args) >= 2 and args[1] == 'short':
    run = run_tests
    args = args[1:]

sys.exit(run('.' if len(args) != 2 else args[1]))

