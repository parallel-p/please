from ..package.package_config import PackageConfig
from ..tests_answer_generator import TestsAndAnswersGenerator
from ..template.template_utils import get_template_full_path
from ..globalconfig import statements_dir, solutions_dir, tests_dir
from ..latex.latex_tools import generate_problem
from logging import getLogger
import glob
import os
import zipfile

_own_tg = TestsAndAnswersGenerator()

TESTDIR = 'tests/'

def inject_checker_validator(zipfile):
    pc = PackageConfig.get_config()
    checker = pc['checker']
    val = pc['validator']
    zipfile.write(checker)
    zipfile.write(val)
    for path in glob.glob('testlib.*'):
        zipfile.write(path)

def inject_tests(zipfile):
    for test, answer in _own_tg.generate_all():
        basetest = os.path.basename(test)
        baseans = os.path.basename(answer)
        zipfile.write(test, TESTDIR + basetest)
        zipfile.write(answer, TESTDIR + baseans)

def inject_tex(zipfile):
    pdf_out = generate_problem()
    tex = os.path.splitext(pdf_out)[0] + '.tex'
    zipfile.write(pdf_out, os.path.basename(pdf_out))
    zipfile.write(tex, os.path.basename(tex)) # TODO it will be uncompilable
    zipfile.write(get_template_full_path('olymp.sty'), 'olymp.sty')

EXCLUDE = [statements_dir, solutions_dir, tests_dir]
SOURCE = 'source/'

logger = getLogger('please_logger.zip')

def inject_source(zipfile):
    for root, dirs, files in os.walk(os.curdir):
        for file in files:
            if file.endswith('.zip') or file.startswith('.'):
                continue
            full = os.path.join(root, file)
            zipfile.write(full, SOURCE + os.path.normpath(full))
            logger.info('%s written', full)
        if root == os.curdir:
            for ex in EXCLUDE:
                try:
                    dirs.remove(ex)
                except ValueError:
                    pass # strange
        new_dirs = []
        for dir in dirs:
            if not dir.startswith('.'):
                new_dirs.append(dir)
        dirs[:] = new_dirs

def inject_solutions(zipfile):
    pc = PackageConfig.get_config(os.curdir)
    for sol in pc['solution']:
        zipfile.write(sol['source'])
    zipfile.write(pc['main_solution'])

def generate_zipfile():
    zip = zipfile.ZipFile('package.zip', 'w')
    inject_solutions(zip)
    inject_tests(zip)
    inject_checker_validator(zip)
    inject_tex(zip)
    inject_source(zip)
    zip.close()
