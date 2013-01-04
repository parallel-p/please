from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from problem.models import Problem
from problem.forms import ManageTestsForm
from problem.helpers import problem_sync
from problem.views.file_utils import *
from problem.views.upload_files import *
from please.command_line.generate_tests import generate_tests, generate_tests_with_tags
import os.path


TESTS_PLEASE_FILENAME = "tests.please"


@problem_sync(read=True, write=False)
def manage_tests(request, id):
    problem = get_object_or_404(Problem.objects, id=id)
    tp_path = os.path.join(problem.path, TESTS_PLEASE_FILENAME)
    if request.method == 'POST':
        form = ManageTestsForm(request.POST)
        if form.is_valid():
            file_write(form.cleaned_data["tests_please_content"], tp_path)

            if "generate_tests" in request.POST:
                stags = form.cleaned_data["tags_for_generate_tests"]
                with ChangeDir(problem.path):
                    if stags != "":
                        generate_tests_with_tags(stags.split(" "))
                    else:
                        generate_tests()
    else:
        form = ManageTestsForm(initial={"tests_please_content": file_read(tp_path)})

    answer = {'manage_tests': {'form': form, 'problem_id': id}}
    answer.update(upload_files(request, id))
    return answer

def manage_tests_page(request, id):
    return render_to_response("manage_tests.html", manage_tests(request, id), RequestContext(request))
