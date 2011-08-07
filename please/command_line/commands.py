PLEASE_VERSION = "0.1"

global_commands = ["create problem PROBLEM_NAME", 
             "export to ejudge contest CONTEST_ID problem[s] PROBLEM_LIST",
             "generate statements PROBLEMS_LIST"]

problem_commands = ["generate statement",
             "generate tests [with tag[s] TAGS_LIST]",
             "generate answers",
             "build all",
             "[show] todo",
             "set standard checker [name]",
             "add tag[s] TAGS_LIST",
             "show tags",
             "clear tags",
             "add solution PATH_TO_SOLUTION expected: EXPECTED_VERDICTS_LIST\n  possible: POSSIBLE_VERDICTS_LIST",
             "add solution PATH_TO_SOLUTION with EXPECTED_VERDICTS_LIST",
             "set main solution PATH_TO_MAIN_SOLUTION",
             "set checker  PATH_TO_CHECKER",
             "set validator PATH_TO_VALIDATOR",
             "check solution PATH_TO_SOLUTION",
             "check solutions",
             "stress test SOLUTION [CORRECT_SOLUTION] GENERATOR",
             "import polygon package PATH_TO_POLYGON_PACKAGE",
             "compute TL",
             "compute integer TL",
             "generate html report",
             "set problem name NAME"]

def print_lite_help(in_problem_folder):
    print("\nUsage: please [command]")
    print("Commands available (try 'please help' for more information):\n")
    for value in global_commands:
        print(value)
    if in_problem_folder:
        for value in problem_commands:
            print(value)

def print_help():
    print("""
Please version {0}
Usage: please [command]

Global commands available:

  {1}:
    Generates file structure of a problem
    (checker, validator, default.package)
    example: please generate problem primes
    
  {2}:
    Exports problem to ejudge
    example: please export to ejudge problem 345348 task primes

  {3}:
    Generates PDF for problems listed. All the tasks must
    be in the directory, where you launch this command
    example: please generate statements island agripina dominoes

Commands available when inside problem's folder:

  {4}:
    Generates pdf statement for current problem
    
  {5}:
    Generates tests for current problem
    example: generate tests
             generate tests with qsort arrays
              
  {6} : Generates answers for all tests in .tests dir
    example : generate answers
             
  {7}:
    Shows TODO and builds everything
    
  {8}:
    Shows TODO
    
  {9}:
    Sets standard checker with name
    Default standard checkers:  acmp.cpp, dcmp.cpp, fcmp.cpp, 
                                hcmp.cpp, icmp.cpp, lcmp.cpp,
                                ncmp.cpp, rcmp4.cpp, rcmp6.cpp,
                                rcmp9.cpp, rcmp.cpp, rncmp.cpp,
                                wcmp.cpp, yesno.cpp
    example: add standard checker acmp
  
  {10}:
    Adds tags to current problem
    example: add tags qsort arrays
    
  {11}:
    Prints all tags associated with current problem
    
  {12}:
    Removes all tags associated with current problem
    
  {13}:
    Adds solution with some expected and possible verdicts
    example: add solution ..\..\sources\solution_tl_ml.cpp expected: TL,ML possible: OK,RE
   
  {14}:
    Adds solution with some expected verdicts and OK possible verdict
    example: add solution ..\sources\solution_wa.cpp with WA

  {15}: 
    Sets main solution (solution that should pass all tests). Copies specified file in \solutions and edits default.package
    example: add main solution ..\..\sources\solution_ok.cpp
   
  {16}: 
    Sets checker. Copies specified file to the problem directory and edits default.package
    example: add checker ..\..\sources\checker.dpr
    
  {17}: 
    Sets validator. Copies specified file to the problem directory and edits default.package
    example: add validator ..\..\sources\validator.cpp
    
  {18}:
    Checks solution specified
    example: check solution solutiontl.cpp
    
  {19}
    Checks all solutions available    
    
  {20}:
    Performs a stress test of current solution
    example: stress test solutions/wrong.cpp "tests/gen.cpp 10 5"
             stress test solutions/wrong.cpp solutions/aa.cpp tests/gen.cpp
  {21}
    Imports Polygon package (in .zip format) to please package"
    example: import polygon package centroid.zip

  {22}
    Computes adequate TL of current problem as doubled maximum running time of main solution

  {23}
    Computes adequate integer TL of current problem as doubled maximum running time of main solution
  
  {24}
    Generates html file report.html. This file contains tables with results of working of all solutions.
  
  {25}
    Sets current problem name
""".format(PLEASE_VERSION, *(global_commands + problem_commands)))
















