from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from problem.helpers import problem_sync
from problem.models import Problem
from problem.views import materials, todo, manage_tests
from please.utils.exceptions import PleaseException


@problem_sync(read=False, write=False)
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
        'problem': problem,
        'edit_dict': materials.edit_dict(request, id),
        'todo': todo.show_block(problem),
        'error': error,
    }, RequestContext(request))


@problem_sync(read=False, write=False)
def tests(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render_to_response('problem/tests.html', {
        'problem': problem,
        'manage_tests': manage_tests.manage_tests(request, problem),
        'todo': todo.show_block(problem),
    }, RequestContext(request))
