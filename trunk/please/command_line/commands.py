from .. import globalconfig

PLEASE_VERSION = globalconfig.please_version

global_commands = ["create problem PROBLEM_NAME",
             "export to ejudge contest CONTEST_ID problem[s] PROBLEM_LIST",
             "generate statements PROBLEMS_LIST",
             "help",
             "[show] todo PATH_TO_PROBLEM",
             "import polygon package PATH_TO_POLYGON_PACKAGE",
             "import polygon problem PROBLEM_LETTER from contest CONTEST_ID",
             "commands",
             "create contest CONTEST_NAME of PROBLEMS",
             ]

contest_commands = ["add problem[s] PROBLEMS to CONTEST [as ALIASES]",
                    "del[ete] problems PROBLEMS from CONTEST",
                    "gen[erate] contest CONTEST statement|pdf",
                    "export CONTEST to SYSTEM as ID",
                    "change contest CONTEST prop[erties] KEY VALUE"]

problem_commands = ["generate statement",
             "generate tests [with tag[s] TAGS_LIST]",
             "generate answers",
             "build all",
             "[show] todo",
             "set standard checker CHECKER_NAME",
             "add tag[s] TAGS_LIST",
             "show tags",
             "clear tags",
             "add solution PATH_TO_SOLUTION [input PATH_OR_STDIN] [output PATH_OR_STDOUT] [possible POSS_VERDICTS_LIST] [expected EXP_VERDICTS_LIST]",
             "",
             "set main solution PATH_TO_MAIN_SOLUTION",
             "set checker PATH_TO_CHECKER",
             "set validator PATH_TO_VALIDATOR",
             "check solution PATH_TO_SOLUTION",
             "check solutions",
             "stress SOLUTION [CORRECT_SOLUTION] GENERATOR",
             "compute TL",
             "compute integer TL",
             "",
             "set problem name NAME",
             "check main solution",
             "clean",
             "validate tests",
             "",
             "del[ete] solution PATH_TO_SOLUTION",
             "change prop[erties] PATH_TO_SOLUTION [ARG VALUES...]",
             "del[ete] prop[erties] PATH_TO_SOLUTION ARGS"
             ]

def print_desc_and_commands(desc, commands):
    print('\n%s\n' % desc)
    print(*[command for command in sorted(commands) if command != ''], sep = '\n')
    
def print_lite_help():
    print("Usage: please [command]")
    print("Commands available (try 'please help' for more information):")
    print_desc_and_commands("Global commands:", global_commands)
    print_desc_and_commands("Problem editing commands:", problem_commands)
    print_desc_and_commands("Contest editing commands:", contest_commands)
    
def print_help():
    print("""
Please version: {0}
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

  {4}:
    Shows this help

  {5}:
    Shows TODO for given problem

  {6}:
    Imports Polygon package (in .zip format) to please package
    example: import polygon package centroid.zip

  {9}:
    Creates new contest of given problems
    example: create contest ioi of ../dynamic/cubes children
    (will create ioi.contest)

  {7}:
    Imports given Polygon problem from given contest
    
  {8}:
    Shows all please commands
""".format(PLEASE_VERSION, *global_commands))
    print("""
Commands available inside problem's folder:

  {0}:
    Generates pdf statement for current problem

  {1}:
    Generates tests for current problem
    example: generate tests
             generate tests with qsort arrays

  {2} : Generates answers for all tests in .tests dir
    example : generate answers

  {3}:
    Shows TODO and builds everything

  {4}:
    Shows TODO

  {5}:
    Sets standard checker with name
    Default standard checkers:  acmp.cpp, dcmp.cpp, fcmp.cpp,
                                hcmp.cpp, icmp.cpp, lcmp.cpp,
                                ncmp.cpp, rcmp4.cpp, rcmp6.cpp,
                                rcmp9.cpp, rcmp.cpp, rncmp.cpp,
                                wcmp.cpp, yesno.cpp
    For more detailed information look at wiki on http://code.google.com/p/please
    example: add standard checker acmp

  {6}:
    Adds tags to current problem
    example: add tags qsort arrays

  {7}:
    Prints all tags associated with current problem

  {8}:
    Removes all tags associated with current problem

  {9}:
    Adds solution with specified properties
    example: add solution solutions/solution_slow.cpp input stdin output test.out expected OK TL 
    
  {25}:
    Deletes solution from default.package
    
  {26}:
    Changes given solution properties
    example: change properties expected OK RE input input.txt
    
  {27}:
    Deletes given solution properties
    example: delete properties input output

  {11}:
    Sets main solution (solution that should pass all tests). Copies specified file in /solutions and edits default.package
    example: add main solution ../../sources/solution_ok.cpp

  {12}:
    Sets checker. Copies specified file to the problem directory and edits default.package
    example: add checker ../../sources/checker.dpr

  {13}:
    Sets validator. Copies specified file to the problem directory and edits default.package
    example: add validator ../../sources/validator.cpp

  {14}:
    Checks solution specified
    example: check solution solutiontl.cpp

  {15}
    Checks all solutions available

  {21}:
    Checks main solution, specified in default.package
    
  {16}:
    Performs a stress testing of current solution
    examples: stress solutions/wrong.cpp tests/gen.cpp 10 5
              stress solutions/wrong.cpp solutions/aa.cpp tests/gen.cpp

  {17}
    Computes adequate TL of current problem as ceiled doubled maximum running time of main solution

  {18}
    Computes adequate integer TL of current problem as doubled maximum running time of main solution
    {19}
  {20}
    Sets current problem name
    {24}
  {21}:
    Checks main solution, specified in default.package
    
  {22}
    Cleans up current directory - removes generated binary files, temporary folders, logs

  {23}:
    Validates all generated tests
""".format(*problem_commands))
    print("""
Commands available for contest editing:

  {0}:
    Adds chosen problems in existing contest
    example: add problems A ../B to roi
    (will add to roi.contest)
    
  {1}:
    Deletes chosen problems in existing contest
    example: del problems A B C from roi
    (will delete from roi.contest)
    
  {2}:
    Generates combined pdf statement
    example: generate contest IOI statement
    (will generate pdf for IOI.contest)
  
  {3}:
    Description will be added later
    
  {4}:
    Changes chosen parameter of given contest
    example: change contest ioi prop name "International Olympiad in Informatics"
""".format(*contest_commands))


