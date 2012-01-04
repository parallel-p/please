import HTML

class HtmlReporter:
    def __init__(self):
        self.__solutions = []
        self.__tests = []
        self.__reports = {}
        pass

    def add_test(self, solution, test, outcome):
        if (not (solution in self.__solutions)):
            self.__solutions.append(solution)
        if (not (test in self.__tests)):
            self.__tests.append(test)
        self.__reports[(solution, test)] = outcome

    def get_str(self, verdicts = [], fail = False):
        row = [HTML.TableCell("tests", bgcolor = 'grey')]
        for solution in self.__solutions:
            row.append(HTML.TableCell(solution, bgcolor = "red" if fail else ""))

        html_table = HTML.Table(header_row=row)

        verdict_to_color = {
            'OK':   'lime',
            'PE':   'red',
            'WA':   'red',
            'RE':   'red',
            'NO':   '',
            'CE':   'orange',
            'TL':   'pink',
            'ML':   'pink',
            'JE':   'maroon',
            'CF':   'olive',
            'real TL':   'windows'
        }
        verdicts_set = set(verdicts)
        if "OK" not in verdicts_set:
            verdict_to_color["OK"] = "red"
        for index in verdict_to_color:
            if index in verdicts_set:
                verdict_to_color[index] = "lime"

        for test in self.__tests:
            row = [HTML.TableCell(test, bgcolor = 'grey')]
            for solution in self.__solutions:
                if ((solution, test) in self.__reports):
                    verdict = self.__reports[(solution, test)].verdict
                else:
                    verdict = "NO"
                colored_ceil = HTML.TableCell(verdict, bgcolor=verdict_to_color[verdict])
                row.append(colored_ceil)
            html_table.rows.append(row)

        html_code = str(html_table)

        return html_code
