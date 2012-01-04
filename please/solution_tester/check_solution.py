import os.path
from ..solution_tester.tester import TestSolution
import logging
import colorama
from colorama import Fore
from ..utils.platform_detector import get_platform
from ..solution_tester.package_config import PackageConfig
from ..invoker import invoker
from .. import globalconfig
from . import solution_config_utils

colorama.init()

logger = logging.getLogger("please_logger.check_solution")

class SolutionNotFoundException(Exception):
    pass

def printc(text, color = Fore.RESET):
    print(color + text + Fore.RESET)
    logger.debug(text)
    
def chunks(l, n):
    """ Yield successive n-sized chunks from l """
    for i in range(0, len(l), n):
        yield l[i:i+n]
        
def get_test_results_from_solution(solution, config = None):

    if config is None:
        config = PackageConfig.get_config()
  
    new_config = solution_config_utils.make_config(solution, config)

    test_solution = TestSolution(new_config)
    met_not_expected, expected_not_met, testing_result = test_solution.test_solution(solution)
    
    return (met_not_expected, expected_not_met, testing_result)

def print_results(test_all_results):
    """
    Takes list of cortages ('solution', test_results)
    Draws table.
    RED text if result is not OK, GREEN text if OK    
    """

    ok_count = 0
    fail_count = 0
    
    for chunk in list(chunks(test_all_results, 3)):
        # Build the header        
        table_header = "| Test # | "
        
        # List of lines each corresponding to a certain test    
        table_lines = {}
        
        # Get test results for all solutions
        for solution in chunk:
            #solution[1] is test results, (met_not_expected, expected_not_met, testing_result)
            #solution[1][2] is testing result
            #solution[0] is path to solution
            #for more information see get_tests_result_from_solution
            testing_result = solution[1][2]
            solution_name = solution[0]
            
            table_header += solution_name + " | "
            
            # Remove unnecessary stuff from test names ("sfsdf/sdfsdf/1" => 1)
            testing_result2 = {}
            for key, value in testing_result.items():
                testing_result2[key.replace("\\", "/").split("/")[1]] = testing_result[key]
            
            # Loop through all results ({1:(invoker.ResultInfo, s, s)}) and print them
            for key, value in sorted(testing_result2.items()):
                # Get test's number and its verdict
                number = int(key)
                result_info = value[0]
                
                # Create a new table line if it hasn't been created yet
                if number not in table_lines:
                    table_lines[number] = ""
            
                # Add test result info to current line with all indents                
                test_result = "{0} T={1:.2f}s RT={2:.2f}s".format(result_info.verdict, result_info.cpu_time, result_info.real_time)  
                
                # Get indents
                indent_verdict = ""      
                for i in range(len(solution_name) - len(test_result) + 1):
                    indent_verdict += " "                       
                             
                if result_info.verdict != "OK":
                    fail_count += 1
                    table_lines[number] += Fore.RED
                else:
                    ok_count += 1
                    table_lines[number] += Fore.GREEN
                table_lines[number] += test_result + indent_verdict + Fore.RESET + "| " 
        
        # Print table header           
        table_header += "\n"
        hor_line = ""
        for i in range(0, len(table_header) - 2):
            hor_line += "-"   
        print("\n" + hor_line + "\n" + table_header + hor_line)
        
        # Print table lines
        for key in sorted(table_lines.keys()):
            indent_number = ""
            for i in range(7 - len(str(key))):
                indent_number += " "
            print("|" + indent_number + str(key) + " | " + table_lines[key])
            print(hor_line)
        
    printc("\nTotal:  %s" % (ok_count + fail_count), Fore.YELLOW)
    printc("Failed: %s" % fail_count,                Fore.RED)
    printc("Passed: %s" % ok_count,                  Fore.GREEN)    

def check_solutions(paths, config = None, print_table = True):
    """
    Calls function test_solution and prints results.
    """

    if config is None:
        config = PackageConfig.get_config()
    
    test_all_results = []
    
    for solution in paths:
        result = get_test_results_from_solution(solution, config)
        test_all_results.append( (solution, result) )
        
    print_results(test_all_results)
        
def check_multiple_solution():
    """ Calls check_solution with different solution paths from config file including main solution """
    config = PackageConfig.get_config()
    
    # Add main solution
    main_solution = config["main_solution"]
    solution_list = []
    solution_list.append(main_solution)
    
    # Add other solutions    
    solutions = config["solution"]
    if solutions != None:
        for solution in solutions:
            # Make sure we don't add main solution that has already been added
            if solution["source"] != main_solution:
                solution_list.append(solution["source"])
    
    # Check them all
    check_solutions(solution_list, config = config)
    
def check_main_solution():
    config = PackageConfig.get_config()
    check_solutions([config["main_solution"]], config = config)
    
# Separate method for command line matcher
def check_solution(path):
    config = PackageConfig.get_config()
    check_solutions([path], config = config)
