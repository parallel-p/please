from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from problem.models import Problem
from problem.forms import ProblemEditForm, ProblemSearch, AddProblemForm, ProblemImportFromPolygonForm
from problem.synchronization import export_from_database, import_to_database, import_tree
from please.template.problem_template_generator import generate_problem
from django.core.exceptions import ObjectDoesNotExist
import os
from problem.views.file_utils import ChangeDir
from please.import_from_polygon import download_zip
from please.import_from_polygon import create_problem


def common(request):
    return render_to_response('problems.html', {
        'navbar': 'problems',
        'problems_list': show_by_tag_block(request),
    }, RequestContext(request))


class NoDirectoryException(Exception):
    pass


class ProblemExistsException(Exception):
    pass


def import_to_database_advanced(model, path):
    template_problem = None
    for problem in Problem.objects.all():
        if problem.name == "Template_problem_for_please":
            template_problem = problem
            break
    if template_problem is None:
        model.save()
        import_to_database(model, path)
    else:
        model = template_problem
    return model


def edit_or_create_problem_block(request, problem=None):
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
        'problem': problem,
    }

def create(request):
    return render_to_response('create_problem.html', edit_or_create_problem_block(request), RequestContext(request))

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

def add(request):
    if request.method == 'POST':
        form = AddProblemForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            problem = Problem(path=path)
            problem.save()
            import_to_database(problem)
            problem.save()
            return redirect('/problems/confirmation')
    else:
        form = AddProblemForm()
    return render_to_response('problem_add.html', {'form': form}, RequestContext(request))


def add_tree(request):
    if request.method == 'POST':
        form = AddProblemForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            return render_to_response('problem_add_tree.html', {
                'form': form,
                'paths': import_tree(path),
            }, RequestContext(request))
    else:
        form = AddProblemForm()
    return render_to_response('problem_add_tree.html', {'form': form}, RequestContext(request))


def problems_list(problems):
    return render_to_response("problems_list.html", {"problems": problems})


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
    else:
        form = ProblemImportFromPolygonForm()
    return {'import_from_polygon': {'form': form}}


def import_from_polygon(request):
    return render_to_response('problems_polygon_import.html', import_from_polygon_block(request),
            context_instance=RequestContext(request))
