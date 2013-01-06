from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from problem.helpers import problem_sync
from problem.models import Problem
from problem.views import materials, todo, manage_tests, files
from problem.views.solutions import upload_solution, retest_solutions
from problem.views.problems import edit_or_create_problem_block, show_tests_block
from problem.views.tags import process_edit_tags
from please.utils.exceptions import PleaseException
from problem.views.file_utils import ChangeDir
from please.build_all import build_tools
from django.core.urlresolvers import reverse
from problem.views.tags import process_edit_tags


@problem_sync(read=True, write=False)
def settings(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render_to_response('problem/settings.html', {
        'nav': 'settings',
        'problem': problem,
        'edit_problem': edit_or_create_problem_block(request, problem),
        'edit_tags': process_edit_tags(request, id),
        'todo': todo.show_block(problem),
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
    }, RequestContext(request))

def build_all_block(request, problem_id):
    button_pressed = False
    error_msg = None
    if request.method == 'POST':
        with ChangeDir(Problem.objects.get(id=problem_id).path):
            build_tools.build_all()
            button_pressed = True
    return {'is_success': button_pressed, 'problem_id': problem_id}


def build_all(request, problem_id):
    block = build_all_block(request, problem_id)
    if block['is_success']:
        return redirect(reverse('problem.views.problems.index'))  # TODO: there?
    return render_to_response('problem/build_all.html', {'build_all': block},
            context_instance=RequestContext(request))
