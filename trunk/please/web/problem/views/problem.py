from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from problem.helpers import problem_sync
from problem.models import Problem
from problem.views import materials, todo, manage_tests, files
from problem.views.solutions import upload_solution, retest_solutions
from problem.views.problems import edit_or_create_problem_block, show_tests_block, please_clean
from problem.views.tags import process_edit_tags
from please.utils.exceptions import PleaseException
from problem.views.file_utils import ChangeDir
from please.build_all import build_tools
from django.core.urlresolvers import reverse


@problem_sync(read=True, write=False)
def settings(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render_to_response('problem/settings.html', {
        'nav': 'settings',
        'problem': problem,
        'edit_problem': edit_or_create_problem_block(request, problem),
        'edit_tags': process_edit_tags(request, id),
        'todo': todo.show_block(problem),
        'files_in_dir': manage_tests.files_in_dir_block(problem),
    }, RequestContext(request))


@problem_sync(read=True, write=False)
def statements(request, id):
    problem = get_object_or_404(Problem, id=id)
    error = None
    if request.method == 'POST' and 'save_and_generate' in request.POST:
        materials.edit_dict(request, id)
        try:
            return materials.gen_statement(request, id)
        except PleaseException as e:
            error = str(e)
    return render_to_response('problem/statements.html', {
        'nav': 'statements',
        'problem': problem,
        'edit_dict': materials.edit_dict(request, id),
        'todo': todo.show_block(problem),
        'files_in_dir': manage_tests.files_in_dir_block(problem),
        'error': error,
    }, RequestContext(request))


@problem_sync(read=True, write=False)
def tests(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render_to_response('problem/tests.html', {
        'nav': 'tests',
        'problem': problem,
        'manage_tests': manage_tests.manage_tests(request, problem),
        'test_data': show_tests_block(request, problem),
        'upload_main': files.upload_main_block(request, problem),
        'todo': todo.show_block(problem),
        'files_in_dir': manage_tests.files_in_dir_block(problem),
    }, RequestContext(request))


@problem_sync(read=True, write=False)
def solutions(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render_to_response('problem/solutions.html', {
        'nav': 'solutions',
        'problem': problem,
        'upload_solution': upload_solution(request, id),
        'retest': retest_solutions(request, id),
        'todo': todo.show_block(problem),
        'files_in_dir': manage_tests.files_in_dir_block(problem),
    }, RequestContext(request))


def build_all_block(request, problem):
    is_success = False
    if request.method == 'POST':
        if 'build' in request.POST:
            with ChangeDir(problem.path):
                build_tools.build_all()
                is_success = True
        if 'clean' in request.POST:
            please_clean(problem)
            is_success = True
    return {'is_success': is_success, 'problem_id': problem.id}


def build_all(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    block = build_all_block(request, problem)
    if block['is_success']:
        return redirect(reverse('problem.views.problem.solutions', kwargs={"id":problem_id}))
    return render_to_response('problem/build_all.html', {'build_all': block},
            context_instance=RequestContext(request))
