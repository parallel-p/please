from ..solution_tester.package_config import PackageConfig
from .. import globalconfig
from .html_report import HtmlReporter
import logging
from ..solution_tester import solution_config_utils
import os.path
from ..solution_tester.tester import TestSolution

logger = logging.getLogger("please_logger.reports.generate_html_report")
def get_test_results_from_solution(solution, config = None):

    if config is None:
        config = PackageConfig.get_config()
        # TODO: check if config is still None
  
    new_config = solution_config_utils.make_config(solution, config)

    test_solution = TestSolution(new_config)
    met_not_expected, expected_not_met, testing_result = test_solution.test_solution(solution)
    
    return (met_not_expected, expected_not_met, testing_result)
def generate_html_for_solution(config, solution, expected = [], possible = []):
    ''' Generates <div> block with tabled report for given solution  '''
    expected = expected or globalconfig.default_expected
    possible = possible or globalconfig.default_possible
    report = get_test_results_from_solution(solution, config)
    html_reporter = HtmlReporter()
    
    for test, checker_verdict in sorted(report[2].items(), key = lambda x: int(os.path.basename(x[0]))):
        html_reporter.add_test(solution, os.path.basename(test), checker_verdict[0])

    footer = ""
    if len(report[0]) > 0:
        footer += "unexpected but met: <b>%s</b><br />" % "</b>,<b> ".join(report[0].keys())
    if len(report[1]) > 0:
        footer += "expected but not met: <b>%s</b><br />" % "</b>,<b> ".join(report[1])

    return "<div style='display: inline; float: left; margin: 5px; font-family: monospace'>" + html_reporter.get_str(expected + possible, fail = len(report[0]) + len(report[1]) > 0) + footer + "</div>"

def generate_html_report(solves, add_main=False):
    html = ''
    config = PackageConfig.get_config()
    
    if add_main:
        html += generate_html_for_solution(config, config["main_solution"])
        
    for solve in solves:
        html += generate_html_for_solution(config, solve["source"], solve["expected"], solve["possible"])
        
    html = "<div style='width: 10000px'>" + html + "</div>"
    with open("report.html", "w", encoding = "utf-8") as output:
        output.write(html)

    logger.info("HTML report is generated and saved as 'report.html' in the root directory of current problem")
