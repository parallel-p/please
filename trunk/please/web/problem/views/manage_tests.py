from problem.models import WellDone
from problem.forms import ManageTestsForm
from problem.views.file_utils import *
from problem.views.upload_files import *
from please.command_line.generate_tests import generate_tests
from please import globalconfig
from please.utils.exceptions import PleaseException
from please.tests_answer_generator.tests_answer_generator import TestsAndAnswersGenerator
from problem.synchronization import export_from_database
import os.path
import re


IGNORED = r'(^\.[\\/]((\.)|(__)))|(\.(exe|pyc|log|config|please|aux|package)$)'


def files_in_dir_block(problem):
    files_in_dir = []
    with ChangeDir(problem.path):
        for dirpath, dirnames, filenames in os.walk("."):
            if re.search(IGNORED, dirpath):
                continue
            for filename in filenames:
                if not re.search(IGNORED, filename):
                    files_in_dir.append(os.path.join(dirpath, filename)[2:])
    files_in_dir.sort()
    return files_in_dir


def manage_tests(request, problem):
    tp_path = os.path.join(problem.path, globalconfig.default_tests_config)
    form = ManageTestsForm()
    error = None

    if request.method == 'POST' and 'manage_tests' in request.POST:
        form = ManageTestsForm(request.POST)
        if form.is_valid():
            file_write(form.cleaned_data["tests_please_content"], tp_path)

            for field, listname in ((problem.well_done_test, 'well_done_test'),
                                    (problem.well_done_answer, 'well_done_answer')):
                field.clear()
                for name in request.POST.getlist(listname):
                    field.add(WellDone.objects.get(name=name))
            problem.save()
            export_from_database(problem)

            try:
                if "generate_tests" in request.POST:
                    with ChangeDir(problem.path):
                        generate_tests()
                elif "validate" in request.POST:
                    with ChangeDir(problem.path):
                        TestsAndAnswersGenerator().validate()
            except PleaseException as e:
                error = e
    else:
        try:
            form = ManageTestsForm(initial={"tests_please_content": file_read(tp_path)})
        except (UnicodeDecodeError, FileNotFoundError) as e:
            error = e

    well_dones = [(well_done.name,
                   well_done in problem.well_done_test.all(),
                   well_done in problem.well_done_answer.all())
                   for well_done in WellDone.objects.all()]

    answer = {'form': form, 'problem': problem, 'error': error, 'well_dones': well_dones}
    answer.update({'upload_files': upload_files(request, problem)})
    return answer
