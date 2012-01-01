from ..import_from_polygon import create_stub
from ..import_from_polygon import create_statements
from ..import_from_polygon import create_code

from ..test_info import cmd_gen_test_info, file_test_info

from ..package import config

import zipfile
from lxml import etree
import os
import shutil
import math
import logging

class PolygonImporter:
    def unzip(self, name, directory):
        """
        This method unzips polygon package and creates problem in please format.
        Problems are created in main Please directory. Method takes sole argument:
        package - path to polygon package to be imported
        """
        zf = zipfile.ZipFile(name)
        zf.extractall(directory)
        os.chdir(directory)
        for file in os.listdir('.'):
            if (file.find('\\') != -1):
                _file = file
                file = file.replace('\\', '/')
                path, who = os.path.split(file)
                try:
                    os.mkdir(path)
                except OSError as e:
                    if (e.errno != 17):
                        raise e
                shutil.move(_file, file)

    def parse_statements(self):
        self.default_package['statement'] = ''
        for statement in self.tree.xpath('/problem/statements/statement'):
            language = statement.get('language')
            path = statement.get('path')
            with open(path, 'r', encoding='UTF-8') as f:
                content = f.read()
            create_statements.add_statement(self.default_package, language, content, self.cwd)

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
            return cmd_gen_test_info.CmdOrGenTestInfo(generator, attr, tags)

    def make_tests(self):
        tests = []
        for testset in self.tree.xpath('/problem/judging/testset'):
            tag = testset.get('name')
            for i, test in enumerate(testset.xpath('tests/test')):
                tests.append(self.make_TestInfo(i, test, tag))
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

    def create_problem(self, package):
        logger = logging.getLogger("please_logger.import_from_polygon.create_problem")

        self.cwd = os.getcwd()

        path, file_name = os.path.split(package)

        if path != "":
            os.chdir(path)

        directory = '.' + os.path.splitext(file_name)[0]
        self.unzip(file_name, directory)

        self.tree = etree.parse('problem.xml')
        problem = self.tree.xpath('/problem')[0]

        # stub
        name = self.tree.xpath('/problem')[0].get('name')

        if not os.path.exists(os.path.join(self.cwd, name)):
            self.create_default_package(name)

            problem_path = os.path.join(self.cwd, name)
            self.cwd = os.path.join(self.cwd, self.default_package['shortname'])

            self.parse_statements()

            self.make_to_extension()

            tests = self.make_tests()

            self.write_tests(tests)

            self.copy_files()

            self.make_code()

            create_stub.commit_config_file(self.default_package, self.cwd)

            self.fix_creation_time()

        else:

            logger.error("Import error: %s already exists" % name)

        os.chdir('..')
        shutil.rmtree(directory)

        os.chdir(os.path.join(self.cwd, '..'))


    def __init__(self):
        pass

def create_problem(package):
    importer = PolygonImporter()
    importer.create_problem(package)