from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from problem.models import Problem, Test
from problem.forms import TestsForm, AddTestsForm
from problem.helpers import problem_sync
import os
from zipfile import ZipFile


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


def upload_add_file(num, data):
    open(os.path.join(str(problem.path), 'tests', num), 'wb').write(data)

def upload(request, id):
    problem = get_object_or_404(Problem.objects, id=id)
    if request.method == 'POST':
        form = AddTestsForm(request.POST, request.FILES)
        if form.is_valid():
            path = os.path.join(str(problem.path), request.FILES['test'].name)
            open(path, 'wb').write(request.FILES['test'].read())
            if path.endswith('.zip'):
                zfile = ZipFile(path)
                for fname in zfile.namelist():
                    upload_add_file(fname, zfile.open(fname).read())
            else:
                upload_add_file(
                    request.FILES['test'].name,
                    open(path, 'rb').read()
                )
            os.remove(path)
            return redirect('/problems/confirmation/')
    else:
        form = AddTestsForm()
    return render_to_response('add_manual_tests.html', {
            'form': form,
            'id': id
        }, RequestContext(request))
