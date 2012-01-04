from ..import_from_polygon import create_stub
from ..import_from_polygon import create_statements
from ..import_from_polygon import create_code
from ..import_from_polygon import polygon_unzip
from ..test_info import cmd_gen_test_info, file_test_info

from ..package import config

from lxml import etree
import os
import shutil
import math
import logging
from .lang_choice import make_language_choice

class PolygonProblemImporter:
    """def parse_statements(self):
        self.default_package['statement'] = ''
        for statement in self.tree.xpath('/problem/statements/statement'):
            language = statement.get('language')
            path = statement.get('path')
            with open(path, 'r', encoding='UTF-8') as f:
                content = f.read()
            create_statements.add_statement(self.default_package, language, content, self.cwd)
    """
    def parse_statements(self):
        self.default_package['statement'] = ''
        statements = self.tree.xpath('/problem/statements/statement')
        for statement in statements:
            language = statement.get('language')
            path = statement.get('path')
            with open(path, 'r', encoding='UTF-8') as f:
                content = f.read()
            create_statements.add_statement(self.default_package, language, content, self.cwd)
        to_get = make_language_choice(statements)
        self.default_package['statement'] = "statements/statement."+to_get.get('language')+".tex"

    def make_to_extension(self):
        # making file -> file.ext dictionary
        self.to_extension = {}
        for exe in self.tree.xpath('/problem/files/executables/executable'):
            source = exe.xpath('source/file')[0].get('path')
            without_ext = source[6:source.rfind('.')]           
            self.to_extension[without_ext] = source[6:]

    def make_TestInfo(self, i, test, tag):
        tags = {tag : None}
        if (test.get('method') == 'manual'):
            test_id = "{0:02d}".format(i + 1) #maybe bad, to think about
            new_test_id = tag + '_' + str(i + 1)
            shutil.copy(os.path.join(tag, test_id), \
                        os.path.join(self.cwd, 'tests', new_test_id))
            # cross-platform
            return file_test_info.FileTestInfo('tests/' + new_test_id, tags)
        else:
            cmd = test.get('cmd').split()
            generator = self.to_extension[cmd[0]]
            attr = cmd[1:]
            cur_output_file = test.get('from-file')
            if cur_output_file:
                tags['mask'] = str(cur_output_file) + '$'
            return cmd_gen_test_info.CmdOrGenTestInfo(generator, attr, tags)

    def make_tests(self):
        raw_tests = []
        for testset in self.tree.xpath('/problem/judging/testset'):
            tag = testset.get('name')
            for i, test in enumerate(testset.xpath('tests/test')):
                raw_tests.append(self.make_TestInfo(i, test, tag))
        
        #optimize multigenerators
        tests = []
        for curtest in raw_tests:
            if type(curtest) != cmd_gen_test_info.CmdOrGenTestInfo:
                tests.append(curtest)
                continue
            does = False
            for prevtest in tests:
                if type(prevtest) != cmd_gen_test_info.CmdOrGenTestInfo:
                    continue
                if prevtest == curtest:
                    does = True
                    if 'mask' in prevtest.get_tags() and 'mask' in curtest.get_tags():                       
                        prevtest.set_tag('mask', prevtest.get_tags()['mask']+'|'+curtest.get_tags()['mask'])
                    elif 'mask' in prevtest.get_tags() or 'mask' in curtest.get_tags():
                        prevtest.set_tag('mask', prevtest.get_tags()['mask'] or curtest.get_tags()['mask'])
                    else:
                        pass
            if not does:
                tests.append(curtest)
                
        return tests

    def write_tests(self, tests):
        with open(os.path.join(self.cwd, "tests.please"), 'w') as f:
            for test in tests:
                f.write(test.to_please_format() + '\n')

    def copy_files(self):
        for resource in self.tree.xpath('/problem/files/resources/file'):
            create_code.copy_resource(self.default_package, self.cwd, resource.get('path'))

    def make_code(self):
        checker = self.tree.xpath('/problem/assets/checker/source')[0]
        create_code.copy_checker(self.default_package, self.cwd, checker.get('path'))

        validator = self.tree.xpath('/problem/assets/validator/source')
        # we may have no validators
        if len(validator) > 0:
            validator = validator[0]
            create_code.copy_validator(self.default_package, self.cwd, validator.get('path'))

        for source in self.tree.xpath('/problem/files/executables/executable/source/file'):
            create_code.copy_source(self.default_package, self.cwd, source.get('path'))

        for solution in self.tree.xpath('/problem/assets/solutions/solution'):
            tag = solution.get('tag')
            source = solution.xpath('source')[0]
            path = source.get('path')
            create_code.copy_solution(self.default_package, self.cwd, path, tag)

    def fix_creation_time(self):
        # fixing creation time
        time = None
        with open(os.path.join(self.cwd, '.please', 'time.config'), 'r', encoding='UTF-8') as f:
            time = float(f.read())

        if (time is None):
            raise Exception("time.config not found")
        time = time - 100

        with open(os.path.join(self.cwd, '.please', 'time.config'), 'w', encoding='UTF-8') as f:
            f.write(str(time))

        # fixed

    def create_default_package(self, name):
        judging = self.tree.xpath('/problem/judging')[0]
        in_file = judging.get('input-file')
        out_file = judging.get('output-file')
        tl = judging.xpath('testset/time-limit')[0].text
        tl = math.ceil(float(tl) / 1000)
        ml = judging.xpath('testset/memory-limit')[0].text
        ml = math.ceil(float(ml) / (1 << 20))
        tags = [tag.get('value') for tag in self.tree.xpath('/problem/tags/tag')]

        self.default_package = create_stub.create_stub(name, tl, ml, in_file, out_file, tags, self.cwd)
        
    def import_with_tree(self):
        name = self.tree.xpath('/problem')[0].get('name')

        self.create_default_package(name)

        problem_path = os.path.join(self.cwd, name)
        self.cwd = os.path.join(self.cwd, self.default_package['shortname']) #wtf? do we use name or shortname?

        self.parse_statements()

        self.make_to_extension()

        tests = self.make_tests()

        self.write_tests(tests)

        self.copy_files()

        self.make_code()

        create_stub.commit_config_file(self.default_package, self.cwd)

        #self.fix_creation_time()

    
    def import_from_dir(self, directory, problem_path):
        self.cwd = problem_path
        prev_dir = os.getcwd()
        os.chdir(directory)
        
        self.tree = etree.parse('problem.xml')
        problem = self.tree.xpath('/problem')[0]

        # stub
        name = self.tree.xpath('/problem')[0].get('name')
        
        imported = False
        
        if not os.path.exists(os.path.join(problem_path, name)):
            self.import_with_tree()
            imported = True
        else:
            self.logger.error("Import error: %s already exists" % name)
        
        os.chdir(prev_dir)

        if imported:
            self.logger.warning('Imported polygon package %s' % name)

    def create_problem(self, package):
        prev_dir = os.getcwd()

        path, file_name = os.path.split(package)

        if path != "":
            os.chdir(path)

        directory = '.' + os.path.splitext(file_name)[0]
        polygon_unzip.unzip(file_name, directory)
        
        self.import_from_dir(directory, prev_dir)
        
        shutil.rmtree(directory)

        os.chdir(prev_dir)


    def __init__(self):
        self.logger = logging.getLogger("please_logger.import_from_polygon.create_problem")


def create_problem(package):
    importer = PolygonProblemImporter()
    importer.create_problem(package)