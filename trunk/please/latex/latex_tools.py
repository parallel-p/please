from .. import globalconfig
from ..solution_tester import package_config
import subprocess
import os
from ..template.template_utils import get_template_full_path, make_statement_name
import shutil
from ..executors import runner
from ..tests_generator.tests_generator import TestsGenerator
from ..language_configurator.language_configurator_utils import is_windows
from ..tests_answer_generator.tests_answer_generator import TestsAndAnswersGenerator
from ..utils import form_error_output
import re
import logging

log = logging.getLogger("please_logger.latex.latex_tools")

class LatexError(runner.RunnerError):
    pass

def generate_contest(problem_names = ['.'], template = None, template_vars = globalconfig.default_template_vars, file = None):
    problem_template_path = get_template_full_path(globalconfig.default_template_contest)

    with open(problem_template_path, "r", encoding = "UTF8") as template:
        contest = LatexContestConstructor(template.read(), template_vars)
    single_problem = (problem_names == ["."])

    current_dir = os.getcwd()
    for problem in problem_names:
        os.chdir(problem)
        package_conf = package_config.PackageConfig.get_config()
        # TODO: check if package_conf is None
        problem = SingleProblemCreator(config = package_conf)
        contest.add_problem(problem)
        if not single_problem:
            os.chdir(current_dir)

    if not os.path.exists(globalconfig.temp_statements_dir):
        os.mkdir(globalconfig.temp_statements_dir)

    os.chdir(globalconfig.temp_statements_dir)

    if file is not None:
        new_tex_name = file + ".tex"
    elif single_problem:
        new_tex_name = os.path.basename(package_conf["statement"])
    else:
        new_tex_name = "_".join(problem_names) + ".tex"
    with open(new_tex_name, "w", encoding = "UTF8") as new_tex:
        new_tex.write(contest.construct())

    converter = Latex2Pdf()
    converter.convert(new_tex_name)

    os.chdir(current_dir)

    if file is not None:
        pdf_out_name = os.path.join(globalconfig.temp_statements_dir, file + ".pdf")
    else:
        pdf_out_name = os.path.join(globalconfig.temp_statements_dir, os.path.splitext(new_tex_name)[0] + ".pdf")
    if single_problem:
        shutil.copy(pdf_out_name, os.path.join(globalconfig.statements_dir, os.path.splitext(new_tex_name)[0] + ".pdf"))
    else:
        shutil.copy(pdf_out_name, os.path.splitext(new_tex_name)[0] + ".pdf")
    #os.remove(statement_name)
    log.info("PDF %s was created successfully", os.path.splitext(new_tex_name)[0] + ".pdf")
    return pdf_out_name

class LatexConstructor:
    """
    Creates string contains tex file with problem statement

    a  = LatexConstructor("Vasya wants to find a sum a+b. Help him!")
    a.set_time_limit("2 second")
    a.set_memory_limit("256 MB")
    a.set_new_replace("#{author_name}", "Andrey Sergeevitch")
    a.add_example("10 4", "14")
    a.add_example("3 -3", "0")
    a.add_example("2 2", "4")
    tex_file = a.construct()
    tex_file contains a string with problem statement in tex format

    PROFIT!
    """
    def __init__(self, problem_template):
        self.__problem_template = problem_template
        self.__input_example = []
        self.__output_example = []
        self.__replacements = {}
        self.__example_environment = 'example'
        self.__example_tag = '#{example}'
        # tag to cut notes and paste them after examples

    def add_example(self, input_example, output_example):
        self.__input_example.append(input_example)
        self.__output_example.append(output_example)

    def construct(self):
        """
            returns string, which contains tex file.
            changes template word in this string (for example "#{time_limit}", ...) to the names.
        """
        result = self.__problem_template
        for tag, value in self.__replacements.items():
            result = result.replace(tag, str(value))

        if self.__input_example: #if at least one sample test exists
            examples = "%s\n\\begin{%s}\n" % ('', self.__example_environment)
            count = 0
            for in_example, out_example in zip(self.__input_example, self.__output_example):
                examples += "\\exmp{\n%s}{%s}%%\n" % (str(in_example), str(out_example))
                count += 1
            examples += "\\end{%s}\n" % (self.__example_environment)
            examples = ("\\Example\n" if count == 1 else "\\Examples\n") + examples
        else:
            examples = ''

        result = result.replace(self.__example_tag, examples)
        return result

    def set_new_replace(self, tag, value):
        self.__replacements[tag] = value

    def set_time_limit(self, time_limit):
        self.set_new_replace("#{time_limit}", time_limit)

    def set_memory_limit(self, memory_limit):
        self.set_new_replace("#{memory_limit}", memory_limit)

    def set_input_file(self, input_file):
        self.set_new_replace("#{input_file}", input_file)

    def set_output_file(self, output_file):
        self.set_new_replace("#{output_file}", output_file)

    def set_title(self, title):
        self.set_new_replace("#{title}", title)

    def set_id(self, id):
        self.set_new_replace("#{id}", id)

    def set_text(self, text):
        ''' Divides given text into 2 groups: text and notes. This is very useful if we want to put notes after examples  '''
        matcher = re.compile(r"(.*)(\\Note.*)", re.DOTALL)
        matches = re.search(matcher, text)
        if matches is not None:
            self.set_new_replace("#{text}", matches.group(1))
            self.set_new_replace("#{notes}", matches.group(2))
        else:
            self.set_new_replace("#{text}", text)
            self.set_new_replace("#{notes}", "")

class LatexContestConstructor:
    """
        Description: generate the whole contest by template from given problem
            & selected attributes (title, location, date, separator between problems)
        Usage:
            contest_template = "Title: #{contest_title}\n\
                Location: #{contest_location}\n\
                Date: #{contest_date}\n\
                Problems: #{contest_problem}"
            contest = LatexContestConstructor(contest_template, None, None, None, "\n")
            contest.set_title("My contest")
            contest.set_location("Pandora")
            contest.set_date("20.12.2012")
            contest_in_tex = contest.construct()
    """
    def __init__(self, template, template_vars = {}, separator="\n\\newpage\n"):
        empty_str = ""
        self.__attributes = {}
        self.__list = []
        self.__template = str(template)
        self.__separator = str(separator)
        for index, value in template_vars.items():
            self.__attributes["#{tpl_%s}" % index] = value

    def set_title(self, title):
        self.__attributes["#{tpl_name}"] = str(title)

    def set_location(self, location):
        self.__attributes["#{tpl_location}"] = str(location)

    def set_date(self, date):
        self.__attributes["#{tpl_date}"] = str(date)

    def set_separator (self,separator):
        self.__separator = separator

    def add_problem(self,problem):
        self.__list.append(problem())

    def construct(self):
        """Returns constructed contest"""
        # create a copy of template
        constructed = self.__template
        # replace all entries
        for tag, value in self.__attributes.items():
            # converting random type to string
            constructed = constructed.replace(tag, "{%s}" % str(value))
        constructed = constructed.replace("#{contest_problems}", self.__separator.join(self.__list))
        return constructed

class Latex2Pdf:
    """
        Description: convert given TeX-file to pdf and create pdf-file
        Usage:
            converter = Latex2Pdf()
            converter.convert("MyFile.tex")
    """
    def convert(self, path_to_tex_file):
        log.info("Generating pdf from tex...")
        encoding = "utf8"
        if is_windows():
            os.putenv("TEXINPUTS", get_template_full_path(''))
            encoding = "1251"
        else:
            os.putenv("TEXINPUTS", get_template_full_path('') + ":.:")
        for i in range(2):
            # necessary two iterations for pages counting
            invoke_info, stdout, stderr = runner.run(path_to_tex_file, encoding = encoding)
            print(invoke_info)
            if invoke_info.return_code != 0:
                    raise LatexError(form_error_output.process_err_exit(
                        "Couldn't generate pdf from tex %s" % path_to_tex_file,
                        invoke_info.verdict,
                        invoke_info.return_code,
                        stdout, stderr))

def get_time_string(time):
    #TODO: fix for multilang
    if time % 100 in range(10, 20):
        return "секунд"
    elif time % 10 in range(2, 5):
        return "секунды"
    elif time % 10 == 1:
        return "секунда"
    else:
        return "секунд"

def get_memory_string(memory):
    if memory % 100 in range(10, 20):
        return "мегабайт"
    elif memory % 10 in range(2, 5):
        return "мегабайта"
    else:
        return "мегабайт"

class SingleProblemCreator():
    __name__ = "SingleProblemCreator"

    def __init__(self, config = None, path = '.'):
        self.__config = config
        self.__path = path

    def __call__(self):
        ''' Creates .PDF for problem '''
        statement_name = self.__config["statement"]
        statement_path = os.path.join(self.__path, statement_name)

        statement_template_path = get_template_full_path(globalconfig.default_template_statement)

        with open(statement_template_path, "r", encoding = "utf-8") as template_file:
            problem = LatexConstructor(template_file.read())

        with open(statement_path, "r", encoding = "utf-8") as problem_file:
            problem.set_text(problem_file.read())

        if self.__config['input'] == 'stdin':
            problem.set_input_file('стандартный ввод')
        else:
            if '_' in self.__config['input'] :
                problem.set_input_file(self.__config['input'].replace("_", "\_"))
            else:
                problem.set_input_file(self.__config['input'])

        if self.__config['output'] == 'stdout':
            problem.set_output_file('стандартный вывод')
        else:
            if "_" in self.__config["output"]:
                problem.set_output_file(self.__config["output"].replace("_", "\_"))
            else:
                problem.set_output_file(self.__config['output'])
        problem.set_memory_limit(self.__config['memory_limit'] + ' ' + get_memory_string(float(self.__config["memory_limit"])))
        problem.set_time_limit(self.__config['time_limit'] + ' ' + get_time_string(float(self.__config["time_limit"])))
        problem.set_title(self.__config['name'])
        if 'id' in self.__config:
            problem.set_id(self.__config['id'])
        else:
            problem.set_id('')

        testans = TestsAndAnswersGenerator().generate(["sample"], "sample", False)

        for test, ans in testans:
            with open(os.path.join(test)) as f:
                test_data = f.read()
            with open(os.path.join(ans)) as f:
                answer_data = f.read()
            problem.add_example(test_data, answer_data)
            os.remove(test)
            os.remove(ans)
            
        return (problem.construct())

