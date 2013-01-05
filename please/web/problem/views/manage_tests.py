from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from problem.models import Problem, WellDone
from problem.forms import ManageTestsForm
from problem.views.file_utils import *
from problem.views.upload_files import *
from please.command_line.generate_tests import generate_tests, generate_tests_with_tags
from please import globalconfig
from please.utils.exceptions import PleaseException
from please.tests_answer_generator.tests_answer_generator import TestsAndAnswersGenerator
from problem.synchronization import export_from_database
import os.path


def manage_tests(request, problem):
    tp_path = os.path.join(problem.path, globalconfig.default_tests_config)
    form = ManageTestsForm()
    error = None

    if request.method == 'POST':
        form = ManageTestsForm(request.POST)
        if form.is_valid():
            file_write(form.cleaned_data["tests_please_content"], tp_path)

            for field, listname in ((problem.well_done_test,'well_done_test'),
                                    (problem.well_done_answer,'well_done_answer')):
                field.clear()
                for name in request.POST.getlist(listname):
                    field.add(WellDone.objects.get(name=name))
            problem.save()
            export_from_database(problem)

            try:
                if "generate_tests" in request.POST:
                    stags = form.cleaned_data["tags"]
                    with ChangeDir(problem.path):
                        if stags != "":
                            generate_tests_with_tags(stags.split(" "))
                        else:
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
