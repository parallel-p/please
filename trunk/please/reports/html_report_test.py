import unittest
from please.reports.html_report import HtmlReporter

class ResultInfo:
    def __init__(self, verdict, return_code=None, real_time=None, cpu_time=None, used_memory=None):
        self.verdict = verdict
        self.return_code = return_code
        self.real_time = real_time
        self.cpu_time = cpu_time
        self.used_memory = used_memory


class Tester(unittest.TestCase):
    def test_generate_html_report(self):
        html_reporter = HtmlReporter()
        html_reporter.add_test("first", "01", ResultInfo("OK"))
        html_reporter.add_test("first", "02", ResultInfo("WA"))
        html_reporter.add_test("first", "03", ResultInfo("RE"))
        html_reporter.add_test("second", "01", ResultInfo("TL"))
        html_reporter.add_test("second", "02", ResultInfo("ML"))
        html_reporter.add_test("second", "03", ResultInfo("CE"))
        html_reporter.add_test("third", "01", ResultInfo("JE"))
        html_reporter.add_test("third", "02", ResultInfo("OK"))
        answer = html_reporter.str()
        with open("html_report_test.html", 'w') as f:
            print(answer, file=f)


if __name__ == "__main__":
    unittest.main()
      