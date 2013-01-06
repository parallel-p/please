from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from please.template.problem_template_generator import generate_problem
from please.import_from_polygon import download_zip, create_problem
from please.template.problem_template_generator import generate_problem
from please.cleaner.cleaner import Cleaner
from please import globalconfig

from problem.models import Problem
from problem.forms import ProblemEditForm, ProblemSearch, AddProblemForm, ProblemImportFromPolygonForm
from problem.synchronization import export_from_database, import_to_database, import_tree, is_problem_path
from problem.views.file_utils import ChangeDir

import os


def index(request):
    return render_to_response('problems/index.html', {
        'navbar': 'problems',
        'problems_list': show_by_tag_block(request),
    }, RequestContext(request))


class NoDirectoryException(Exception):
    pass


class ProblemExistsException(Exception):
    pass


def please_clean(problem):
    with ChangeDir(problem.path):
        Cleaner().cleanup()


def edit_or_create_problem_block(request, problem=None):
    is_success = False
    if request.method == 'POST':
        form = ProblemEditForm(request.POST)
        if form.is_valid():
            if problem is None:
                if not os.path.exists(form.cleaned_data["path"]):
                    raise NoDirectoryException("There is no such directory!")
                if os.path.exists(os.path.join(form.cleaned_data["path"], form.cleaned_data["short_name"])):
                    raise ProblemExistsException("This problem already exists")
                problem = import_to_database(problem, "../templates/Template/")
                problem.path = os.path.join(form.cleaned_data["path"], form.cleaned_data["short_name"])
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


def read_from_file(file_name, LINES_LIMIT, SIZE_LIMIT):
    content = ''
    big_file = False
    with open(file_name, 'r') as f:
        line_id = 0
        while True:
            line = f.readline()
            if line == '' or line_id >= LINES_LIMIT:
                if line_id >= LINES_LIMIT:
                    big_file = True
                    content += '...'
                break
            line_id += 1
            if len(line) >= SIZE_LIMIT:
                big_file = True
                line = line[:SIZE_LIMIT - 1] + '...\n'
            content += line
    return (content, big_file)

def show_tests_block(request, problem):
    SIZE_LIMIT = 40
    LINES_LIMIT = 7

    tests_path = os.path.join(problem.path, globalconfig.temp_tests_dir).replace(os.sep, '/')
    current_test = 1
    test_data = []

    while True:
        input_name = '{}'.format(current_test)
        output_name = '{}.a'.format(current_test)
        input_file = os.path.join(tests_path, input_name)
        output_file = os.path.join(tests_path, output_name)

        if not (os.path.exists(input_file) and os.path.exists(output_file)):
            break

        input_content, is_input_too_big = read_from_file(input_file, LINES_LIMIT, SIZE_LIMIT)
        output_content, is_output_too_big = read_from_file(output_file, LINES_LIMIT, SIZE_LIMIT)

        test_data.append((
            {
                'content': input_content,
                'is_too_big': is_input_too_big,
                'name': input_name,
            },
            {
                'content': output_content,
                'is_too_big': is_output_too_big,
                'name': output_name,
            },
        ))

        current_test += 1

    return test_data


def show_test(request, problem_id, test_name):
    problem = get_object_or_404(Problem, id=problem_id)
    tests_path = os.path.join(problem.path, globalconfig.temp_tests_dir).replace(os.sep, '/')
    test_path = os.path.join(tests_path, test_name)
    response = HttpResponse(FileWrapper(open(test_path, 'rb')), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(test_path))
    return response


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
                archive_name = download_zip.get_problem(
                        form.cleaned_data['contest_id'],
                        form.cleaned_data['problem_letter'].upper())
                problem_name = create_problem(archive_name + ".zip")
            problem_path = os.path.join(form.cleaned_data['target_path'],
                    problem_name)
            problem = Problem(path=problem_path, short_name=problem_name)
            problem.save()
            import_to_database(model=problem)
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
    block = import_from_polygon_block(request)
    if block['is_success']:
        print([x.name for x in Problem.objects.all()])
        return redirect(reverse('problem.views.problems.index'))
    return render_to_response('problems/polygon.html', {
        'polygon': block,
    }, RequestContext(request))

