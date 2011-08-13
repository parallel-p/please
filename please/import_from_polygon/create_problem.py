from ..import_from_polygon import create_stub
from ..import_from_polygon import create_statements
from ..import_from_polygon import create_code
from ..test_config_parser.parser import TestInfo

import please.package.config as config

import zipfile
from lxml import etree
import os
import shutil
import math
import logging

def unzip(name, directory):
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
"""
   This method unzips polygon package and creates problem in please format.
   Problems are created in main Please directory. Method takes sole argument:
   package - path to polygon package to be imported
"""
def create_problem(package):
    logger = logging.getLogger("please_logger.import_from_polygon.create_problem")

    cwd = os.getcwd()

    path, file_name = os.path.split(package)

    if path != "":
        os.chdir(path)

    directory = '.' + os.path.splitext(file_name)[0]
    unzip(file_name, directory)

    tree = etree.parse('problem.xml')
    problem = tree.xpath('/problem')[0]

    # stub
    name = tree.xpath('/problem')[0].get('name')

    if not os.path.exists(os.path.join("..", name)):
        in_file = tree.xpath('/problem/judging')[0].get('input-file')
        out_file = tree.xpath('/problem/judging')[0].get('output-file')
        tl = tree.xpath('/problem/judging/testset/time-limit')[0].text
        tl = math.ceil(float(tl) / 1000)
        ml = tree.xpath('/problem/judging/testset/memory-limit')[0].text
        ml = math.ceil(float(ml) / (1 << 20))
        tags = [tag.get('value') for tag in tree.xpath('/problem/tags/tag')]

        default_package = create_stub.create_stub(name, tl, ml, in_file, out_file, tags, cwd)

        problem_path = os.path.join(cwd, name)
        cwd = os.path.join(cwd, default_package['shortname'])
        
        
        # statements
        default_package['statement'] = ''
        for statement in tree.xpath('/problem/statements/statement'):
            language = statement.get('language')
            path = statement.get('path')
            with open(path, 'r', encoding='UTF-8') as f:
                content = f.read()
            create_statements.add_statement(default_package, language, content, cwd)

        # making file -> file.ext dictionary
        to_extension = {}
        for exe in tree.xpath('/problem/files/executables/executable'):
            source = exe.xpath('source/file')[0].get('path')
            without_ext = source[6:source.rfind('.')]
            
            to_extension[without_ext] = source[6:]

        # tests
        
        tests = []
        for testset in tree.xpath('/problem/judging/testset'):
            tag = testset.get('name')
            for i, test in enumerate(testset.xpath('tests/test')):
                attributes = {tag : None}
                if (test.get('method') == 'manual'):
                    test_id = "{0:02d}".format(i + 1)
                    new_test_id = tag + '_' + str(i + 1)
                    shutil.copy(os.path.join(tag, test_id), \
                                os.path.join(cwd, 'tests', new_test_id))
                    type = 'file'
                    # cross-platform
                    command = 'tests/' + new_test_id
                else:
                    type = 'generator'
                    cmd = test.get('cmd').split()
                    command = (to_extension[cmd[0]], cmd[1:])
                testinfo = TestInfo()
                testinfo.constructor({tag : None}, type, command)
                tests.append(testinfo)

        with open(os.path.join(cwd, "tests.please"), 'w') as f:
            for test in tests:
                f.write(str(test) + '\n')

        # files
        for resource in tree.xpath('/problem/files/resources/file'):
            create_code.copy_resource(default_package, cwd, resource.get('path'))

        checker = tree.xpath('/problem/assets/checker/source')[0]
        create_code.copy_checker(default_package, cwd, checker.get('path'))

        validator = tree.xpath('/problem/assets/validator/source')
        # we may have no validators
        if len(validator) > 0:
            validator = validator[0]
            create_code.copy_validator(default_package, cwd, validator.get('path'))

        for source in tree.xpath('/problem/files/executables/executable/source/file'):
            create_code.copy_source(default_package, cwd, source.get('path'))

        for solution in tree.xpath('/problem/assets/solutions/solution'):
            tag = solution.get('tag')
            source = solution.xpath('source')[0]
            path = source.get('path')
            create_code.copy_solution(default_package, cwd, path, tag)

        create_stub.commit_config_file(default_package, cwd)
    
        # fixing creation time
        time = None
        with open(os.path.join(cwd, '.please', 'time.config'), 'r', encoding='UTF-8') as f:
            time = float(f.read())
        
        if (time is None):
            raise Exception("time.config not found")
        time = time - 100
        
        with open(os.path.join(cwd, '.please', 'time.config'), 'w', encoding='UTF-8') as f:
            f.write(str(time))
        
        # fixed

    
    else:
        logger.error("Import error: %s already exists" % name)

    os.chdir("..")

    shutil.rmtree(directory)
