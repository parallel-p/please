import os.path
from ..solution_tester.tester import TestSolution
import logging
import colorama
from colorama import Fore
from ..utils.platform_detector import get_platform
from ..solution_tester.package_config import PackageConfig
from ..invoker import invoker
from .. import globalconfig

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
    if config == None:
        config = PackageConfig.get_config()
    
    # Get results from test_solution, create a config file to send.
    # Find all attributes from config's root or embedded solution's config        
    new_config = {}
    new_config["checker"] = config["checker"]
    new_config["tests_dir"] = globalconfig.temp_tests_dir #config["tests_dir"]        
    
    if os.path.normpath(solution) in os.path.abspath(config["main_solution"]):
        #print("MAIN SOLUTION " + solution)
        new_config["expected_verdicts"] = ["OK"]
        new_config["optional_verdicts"] = []
        new_config["execution_limits"]  = invoker.ExecutionLimits(float(config["time_limit"]), float(config["memory_limit"]))
        new_config["solution_config"] = {"input":config["input"], "output":config["output"]}
        new_config["solution_args"] = []
        solution = os.path.abspath(config["main_solution"])
    else:
        for sol_found in config["solution"]:
            if os.path.normpath(solution) in os.path.abspath(sol_found["source"]):
                #print("SOLUTION FOUND: " + sol_found["source"])               
                new_config["expected_verdicts"] = sol_found["expected_verdicts"]
                new_config["optional_verdicts"] = sol_found["possible_verdicts"]
                new_config["execution_limits"]  = invoker.ExecutionLimits(float(config["time_limit"]), float(config["memory_limit"]))
                new_config["solution_config"] = {"input":config["input"], "output":config["output"]}
                new_config["solution_args"] = []
                solution = os.path.abspath(sol_found["source"])
                break   
        else:
            raise SolutionNotFoundException(solution + ' not found in config')

    test_solution = TestSolution(new_config)
    met_not_expected, expected_not_met, testing_result = test_solution.test_solution(solution)
    
    return (met_not_expected, expected_not_met, testing_result)
    

# Separate method for command line matcher
def check_solution(path):
    check_one_solution(path)

def check_one_solution(*paths, config = None, print_table = True):
    """
    Calls function test_solution and prints results to log and to console.
    RED text if result is not OK, GREEN text if OK    
    """
    ok_count = 0
    fail_count = 0

    if config is None:
        config = PackageConfig.get_config()
    
    # Split the paths into chunks, 3 in each and print them    
    for chunk in list(chunks(paths, 3)):
        # Build the header        
        table_header = "| Test # | "
        
        # List of lines each corresponding to a certain test    
        table_lines = {}
        
        # Get test results for all solutions
        for solution in chunk:
            testing_result = get_test_results_from_solution(solution, config)[2]
            #print("TESTING RESULT: " + str(testing_result))
            
            table_header += solution + " | "
            
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
                for i in range(len(solution) - len(test_result) + 1):
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
    check_one_solution(*solution_list, config = config)
    
    
    
def check_main_solution():
    config = PackageConfig.get_config()
    check_one_solution(config["main_solution"], config = config)
    
    
    
