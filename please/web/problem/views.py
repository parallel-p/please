from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from problem.helpers import problem_sync
from problem.forms import (
    ProblemEditMaterialsForm,
    ProblemSearch,
    ProblemUploadFilesForm,
    ProblemEditForm,
    SolutionAddForm,
    TestsForm
)
import problem
from problem.models import Problem
from please.template.problem_template_generator import *
from problem.synchronization import *
from please.todo.todo_generator import TodoGenerator
import os
import os.path
from os import chdir


@problem_sync(read=False, write=False)
def todo(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render_to_response('todo.html', {
        'status_description': TodoGenerator.get_status_description(problem.path),
        'tests_count': TodoGenerator.generated_tests_count(problem.path),
        'samples_count': TodoGenerator.generated_sample_tests_count(problem.path),
    })

def create_problem(request):
    if request.method == 'POST':
        form = ProblemEditForm(request.POST)
        if form.is_valid():
            cur_path = os.getcwd()
            chdir(form.cleaned_data["path"])
            generate_problem(form.cleaned_data["name"])
            chdir(cur_path)
            model = form.save()
            model.path += model.name
            export_from_database(model)
            return redirect('/problem/confirmation/')
    else:
        form = ProblemEditForm()
    return render_to_response('create_problem.html', {
            'form': form
        }, RequestContext(request))


def add_problem_files(request, id):
    model = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = ProblemUploadFilesForm(request.POST, request.FILES)
        if form.is_valid() and len(request.FILES) > 0:
            if 'checker' in request.FILES.keys():
                checker_fpath, checker_fname = os.path.split(str(model.checker_path))
                checker_fname = request.FILES['checker'].name
                model.checker_path = os.path.join(checker_fpath, checker_fname)
                open(os.path.join(
                        str(model.path),
                        str(model.checker_path)
                    ), 'wb').write(request.FILES['checker'].read())
            if 'validator' in request.FILES.keys():
                validator_fpath, validator_fname = os.path.split(str(model.validator_path))
                validator_fname = request.FILES['validator'].name
                model.validator_path = os.path.join(validator_fpath, validator_fname)
                open(os.path.join(
                        str(model.path),
                        str(model.validator_path)
                    ), 'wb').write(request.FILES['validator'].read())
            model.save()
            return redirect('/problem/confirmation/')
    else:
        form = ProblemUploadFilesForm()
    return render_to_response('add_problem_files.html', {
            'form': form,
            'model': model,
            'id': id
        }, RequestContext(request))


def edit_problem_materials(request, id):
    model = Problem.objects.get(id=id)
    statement_abspath = os.path.join(str(model.path), str(model.statement_path))
    description_abspath = os.path.join(str(model.path), str(model.description_path))
    analysis_abspath = os.path.join(str(model.path), str(model.analysis_path))

    def load_files():
        exc_str = "Could not create {} file (wrong file path field?)"
        if not os.path.exists(statement_abspath):
            try:
                open(statement_abspath, 'w')
            except:
                raise Exception(exc_str.format('statement'))
        if not os.path.exists(description_abspath):
            try:
                open(description_abspath, 'w')
            except:
                raise Exception(exc_str.format('description'))
        if not os.path.exists(analysis_abspath):
            try:
                open(analysis_abspath, 'w')
            except:
                raise Exception(exc_str.format('analysis'))
        return (
            open(statement_abspath, 'r').read(),
            open(analysis_abspath, 'r').read(),
            open(description_abspath, 'r').read()
        )

    if request.method == 'POST':
        form = ProblemEditMaterialsForm(request.POST)
        if form.is_valid():
            open(statement_abspath, 'w').write(form.cleaned_data["statement"])
            open(description_abspath, 'w').write(form.cleaned_data["description"])
            open(analysis_abspath, 'w').write(form.cleaned_data["analysis"])
            # Here we have to do "git commit".
            return redirect('/problem/confirmation/')
    else:
        vals = load_files()
        form = ProblemEditMaterialsForm(initial={
            'statement': vals[0],
            'description': vals[2],
            'analysis': vals[1]
        })
    return render_to_response('edit_problem_materials.html', {
            'form': form
        }, RequestContext(request))


def problems_list(problems):
    return render_to_response("problems_list.html", {"problems": problems})


def problems_search_by_tag(request):
    form = ProblemSearch(request.GET)
    form.is_valid()
    if form.cleaned_data["tags"] == "":
        return render_to_response("problems_search_by_tag.html", {
            "form": form,
            "problems": Problem.objects.all()
        })
    else:
        return problems_list(Problem.objects.filter(tags__name__contains=form.cleaned_data["tags"]).distinct())


def add_solution(request, id):
    if request.method == 'POST':
        form = SolutionAddForm(request.POST)
        form.problem = Problem.objects.get(id=id)
        if form.is_valid():
            form.save()
            return redirect('/problems/{}/'.format(id))
    else:
        form = SolutionAddForm()
    return render_to_response('add_solution.html', {'form': form},
        context_instance=RequestContext(request))


def tests(request, id):
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
    }, RequestContext(request))


def upload_additional():
    form = problem.forms.AdditonalUpload()
