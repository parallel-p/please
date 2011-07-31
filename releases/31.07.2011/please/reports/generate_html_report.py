from ..solution_tester.check_solution import get_test_results_from_solution
from ..solution_tester.package_config import PackageConfig
from .html_report import HtmlReporter

import os.path

def generate_html_for_solution(config, solution, expected_verdicts = ["OK"], possible_verdicts = []):
    ''' Generates <div> block with tabled report for given solution  '''
    report = get_test_results_from_solution(solution, config)
    html_reporter = HtmlReporter()

    if expected_verdicts is None:
        expected_verdicts = []
    if possible_verdicts is None:
        possible_verdicts = []

    impossible_met = set()
    for test, checker_verdict in sorted(report.items(), key = lambda x: int(os.path.basename(x[0]))):
        invoker_verdict = checker_verdict[0]
        if invoker_verdict.verdict in expected_verdicts:
            expected_verdicts.remove(invoker_verdict.verdict)
        if not invoker_verdict.verdict in possible_verdicts:
            impossible_met.add(invoker_verdict.verdict)
        html_reporter.add_test(solution, os.path.basename(test), invoker_verdict)

    footer = ""
    if len(impossible_met) > 0:
        footer += "unexpected but met: <b>%s</b><br />" % "</b>,<b> ".join(impossible_met)
    if len(expected_verdicts) > 0:
        footer += "expected but not met: <b>%s</b><br />" % "</b>,<b> ".join(expected_verdicts)

    return "<div style='display: inline; float: left; margin: 5px; font-family: monospace'>" + html_reporter.str() + footer + "</div>"

def generate_html_report():
    config = PackageConfig.get_config()
    solution = config["main_solution"]

    html = generate_html_for_solution(config, solution)
    generated = set()
    generated.add(solution)

    for solve in config["solution"]:
        if not solve["source"] in generated:
            html += generate_html_for_solution(config, solve["source"], solve["expected_verdicts"], solve["possible_verdicts"])
            generated.add(solve["source"])

    html = "<div style='width: 10000px'>" + html + "</div>"
    with open("report.html", "w", encoding = "UTF8") as output:
        output.write(html)
