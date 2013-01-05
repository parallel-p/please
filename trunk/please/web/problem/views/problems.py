from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from problem.models import Problem
from problem.forms import ProblemEditForm, ProblemSearch, AddProblemForm, ProblemImportFromPolygonForm
from problem.synchronization import export_from_database, import_to_database, import_tree, is_problem_path
from please.template.problem_template_generator import generate_problem
from django.core.exceptions import ObjectDoesNotExist
import os
from problem.views.file_utils import ChangeDir
from please.import_from_polygon import download_zip
from please.import_from_polygon import create_problem


def index(request):
    return render_to_response('problems/index.html', {
        'navbar': 'problems',
        'problems_list': show_by_tag_block(request),
    }, RequestContext(request))


class NoDirectoryException(Exception):
    pass


class ProblemExistsException(Exception):
    pass


def edit_or_create_problem_block(request, problem=None):
    is_success = False
    if request.method == 'POST':
        form = ProblemEditForm(request.POST)
        if form.is_valid():         
            if problem is None:
                problem = Problem()
                if not os.path.exists(form.cleaned_data["path"]):
                    raise NoDirectoryException("There is no such directory!")
                problem.path = os.path.join(form.cleaned_data["path"], form.cleaned_data["short_name"])
                if os.path.exists(problem.path):
                    raise ProblemExistsException("This problem already exists")
                problem.save()
                import_to_database(problem, "../templates/Template/")
                with ChangeDir(form.cleaned_data["path"]):
                    generate_problem(form.cleaned_data["short_name"])
            problem.name = form.cleaned_data["name"]
            problem.short_name = form.cleaned_data["short_name"]
            problem.input = form.cleaned_data["input"]
            problem.output = form.cleaned_data["output"]
            problem.time_limit = float(form.cleaned_data["time_limit"])
            problem.memory_limit = int(form.cleaned_data["memory_limit"])
            problem.save()
            export_from_database(problem)
            is_success = True
    else:
        if problem is None:
            form = ProblemEditForm()
        else:
            form = ProblemEditForm(initial={
                'name': problem.name,
                'short_name': problem.short_name,
                'input': problem.input,
                'output': problem.output,
                'time_limit': problem.time_limit,
                'memory_limit': problem.memory_limit,
            })
    return {
        'form': form,
        'is_success': is_success,
    }

def create(request):
    block = edit_or_create_problem_block(request)
    if block['is_success']:
        return redirect(reverse('problem.views.problems.index'))
    return render_to_response('problems/create.html', {
        'nav': 'create',
        'edit_problem': block,
    }, RequestContext(request))

def show_tests(request, id):
    problem = Problem.objects.get(id=id)
    tests_path = os.path.join(problem.path, ".tests").replace(os.sep, '/')
    tests = []
    for root, dirs, files in os.walk(tests_path):
        for file_name in files:
            if file_name.split('.')[-1] != "a":
                output_file_name = file_name + ".a"
                if output_file_name not in files:
                    output_file_name = None
                tests.append((file_name, output_file_name))

    test_data = []
    for test in tests:
        input_file_data = open(os.path.join(tests_path, test[0]), "r").read()
        if (len(input_file_data) > 255):
            input_file_data = "{}...".format(input_file_data[:254])
        output_file_data = open(os.path.join(tests_path, test[1]), "r").read() if test[1] is not None else ""
        if (len(output_file_data) > 255):
            output_file_data = "{}...".format(output_file_data[:254])
        test_data.append((input_file_data, output_file_data))
                                        
    return render_to_response('problem_tests.html',
                              {'problem_id': id,
                               'data': test_data,
                               }, RequestContext(request))


def add_problem_block(request):
    is_success, is_error = False, False
    if request.method == 'POST':
        form = AddProblemForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            if is_problem_path(path):
                problem = Problem(path=path)
                problem.save()
                import_to_database(problem)
                problem.save()
                is_success = True
            else:
                is_error = True
    else:
        form = AddProblemForm()
    return {
        'form': form,
        'is_success': is_success,
        'is_error': is_error,
    }


def add_tree_block(request):
    if request.method == 'POST':
        form = AddProblemForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            return {
                'form': form,
                'paths': import_tree(path),
            }
    else:
        form = AddProblemForm()
    return {'form': form}


def add(request):
    block = add_problem_block(request)
    if block['is_success']:
        return redirect(reverse('problem.views.problems.index'))
    return render_to_response('problems/add.html', {
        'nav': 'add',
        'add_problem': block,
    }, RequestContext(request))


def add_tree(request):
    return render_to_response('problems/add_tree.html', {
        'nav': 'add_tree',
        'add_problem': add_tree_block(request),
    }, RequestContext(request))


def show_by_tag_block(request):
    form = ProblemSearch(request.GET)
    form.is_valid()
    if form.cleaned_data["tags"] == "":
        problems = Problem.objects.all()
    else:
        problems = Problem.objects.filter(tags__name__contains=form.cleaned_data["tags"]).distinct()
    return {
        'form': form,
        'problems': problems,
    }


def import_from_polygon_block(request):
    is_success = False
    if request.method == 'POST':
        form = ProblemImportFromPolygonForm(request.POST)
        if form.is_valid():
            with ChangeDir(form.cleaned_data['target_path']):
                problem_name = download_zip.get_problem(
                        form.cleaned_data['contest_id'],
                        form.cleaned_data['problem_letter'].upper())
                create_problem(problem_name + ".zip")
            problem_path = os.path.join(form.cleaned_data['target_path'],
                    problem_name)
            problem = Problem(path=problem_path, name=problem_name)
            problem.save()
            import_to_database(model=problem, path=problem_path)
            problem.save()
            form = ProblemImportFromPolygonForm()
            is_success = True
    else:
        form = ProblemImportFromPolygonForm()
    return {
        'form': form,
        'is_success': is_success,
    }


def import_from_polygon(request):
    block =  import_from_polygon_block(request)
    if block['is_success']:
        return redirect(reverse('problem.views.problems.index'))
    return render_to_response('problems/polygon.html', {
        'polygon': block,
    }, RequestContext(request))
