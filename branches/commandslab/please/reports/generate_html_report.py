from ..package.package_config import PackageConfig
from .. import globalconfig
from .html_report import HtmlReporter
import logging
from colorama import Fore
from ..solution_tester import solution_config_utils
import os.path
from ..solution_tester.tester import TestSolution

logger = logging.getLogger("please_logger.reports.generate_html_report")

def printc(text, color = Fore.RESET):
    print(color + text + Fore.RESET)
    logger.debug(text)
    
def chunks(l, n):
    """ Yield successive n-sized chunks from l """
    for i in range(0, len(l), n):
        yield l[i:i+n]

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

def get_test_results_from_solution(config, solution_config):

    new_config = solution_config_utils.make_config_with_solution_config(
        config, solution_config)

    test_solution = TestSolution(new_config)

    actual_path = os.path.join(globalconfig.problem_folder,
                               solution_config.get_path("source"))

    (met_not_expected,
     expected_not_met,
     testing_result) = test_solution.test_solution(actual_path)
    
    return (met_not_expected, expected_not_met, testing_result)

def generate_html_for_solution(config, solution_config):
    ''' Generates <div> block with tabled report for given solution  '''
    report = get_test_results_from_solution(config, solution_config)
    solution = solution_config["source"]
    html_reporter = HtmlReporter()
    
    for test, checker_verdict in sorted(report[2].items(), key = lambda x: int(os.path.basename(x[0]))):
        html_reporter.add_test(solution, os.path.basename(test), checker_verdict[0])

    footer = ""
    if len(report[0]) > 0:
        footer += "unexpected but met: <b>%s</b><br />" % "</b>,<b> ".join(report[0])
    if len(report[1]) > 0:
        footer += "expected but not met: <b>%s</b><br />" % "</b>,<b> ".join(report[1])

    return ["<div style='display: inline; float: left; margin: 5px; font-family: monospace'>" + html_reporter.get_str(fail = len(report[0]) + len(report[1]) > 0) + footer + "</div>", report]

def generate_html_report(solves): # , add_main=False):
    html = ''
    config = PackageConfig.get_config()
    all_results = []
    #if add_main:
    #    gen = generate_html_for_solution(config, config["main_solution"])
    #    html += gen[0]
    #    all_results.append((config["main_solution"], gen[1]))
        
    for solve in solves:
        gen = generate_html_for_solution(config, solve)
        html += gen[0]
        all_results.append((solve["source"], gen[1]))
        
    html = "<div style='width: 10000px'>" + html + "</div>"
    with open("report.html", "w", encoding = "utf-8") as output:
        output.write(html)
    print_results(all_results)
    logger.info("HTML report is generated and saved as 'report.html' in the root directory of current problem")
