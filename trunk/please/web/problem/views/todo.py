from django.shortcuts import render_to_response, get_object_or_404
from problem.helpers import problem_sync
from please.todo.todo_generator import TodoGenerator
from problem.models import Problem


def show_block(problem):
    return {
        'status_description': TodoGenerator.get_status_description(problem.path),
        'tests_count': TodoGenerator.generated_tests_count(problem.path),
        'samples_count': TodoGenerator.sample_tests_count(problem.path),
    }


@problem_sync(read=True, write=False)
def show(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render_to_response('todo.html', {'todo': show_block(problem)})
