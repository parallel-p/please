from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from problem.models import Problem
from problem.forms import ManageTestsForm
from problem.views.file_utils import *
from problem.views.upload_files import *
from please.command_line.generate_tests import generate_tests, generate_tests_with_tags
from please import globalconfig
from please.utils.exceptions import PleaseException
from please.tests_answer_generator.tests_answer_generator import TestsAndAnswersGenerator
import os.path


def manage_tests(request, problem):
    tp_path = os.path.join(problem.path, globalconfig.default_tests_config)
    error = None
    if request.method == 'POST':
        form = ManageTestsForm(request.POST)
        if form.is_valid():
            file_write(form.cleaned_data["tests_please_content"], tp_path)

            try:
                if "generate_tests" in request.POST:
                    stags = form.cleaned_data["tags_for_generate_tests"]
                    with ChangeDir(problem.path):
                        if stags != "":
                            generate_tests_with_tags(stags.split(" "))
                        else:
                            generate_tests()
                elif "validate" in request.POST:
                    stags = form.cleaned_data["tags_for_generate_tests"]
                    with ChangeDir(problem.path):
                        TestsAndAnswersGenerator().validate()
            except PleaseException as e:
                error = e
    else:
        form = ManageTestsForm(initial={"tests_please_content": file_read(tp_path)})

    answer = {'form': form, 'problem_id': problem.id, 'error': error}
    answer.update({'upload_files': upload_files(request, problem)})
    return answer
