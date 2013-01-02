from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from problem.models import Problem
from problem.forms import TestsForm
from problem.helpers import problem_sync
import os.path


@problem_sync(read=True, write=False)
def show(request, id):
    problem = get_object_or_404(Problem.objects, id=id)
    if request.method == 'POST':
        form = TestsForm(request.POST)
        if form.is_valid():
            with open(os.path.join(problem.path, "tests.please"), "w") as tp_file:
                tp_file.write(form.cleaned_data["tests_please_content"])
    else:
        with open(os.path.join(problem.path, "tests.please"), "r") as tp_file:
            content = tp_file.read()
        form = TestsForm(initial={"tests_please_content": content})

    return render_to_response("tests.html", {
        "form": form,
        'problem_id': id,
    }, RequestContext(request))
