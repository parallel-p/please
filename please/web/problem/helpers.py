import os

from django.shortcuts import render_to_response
from problem.models import Problem
from problem import synchronization


def problem_sync(read=True, write=False):
    def wrapped_decorator(function):
        def wrapped_function(request, id, *args, **kwargs):
            problem_was_deleted = False

            if read:
                try:
                    problem = Problem.objects.get(id=id)
                except Problem.DoesNotExist:
                    problem = None
                problem_path = problem.path if problem else None
                if problem:
                    magic_path = os.path.join(problem.path, 'default.package')
                    if not (os.path.exists(magic_path) and
                            problem and
                            os.path.getmtime(magic_path) == problem.magic_modified_value):
                        print('OLOLO', os.path.getmtime(magic_path), '!=',
                              problem.magic_modified_value, 'diff is',
                              os.path.getmtime(magic_path) - problem.magic_modified_value)
                        problem = synchronization.import_to_database(problem)
                        if problem:
                            problem.magic_modified_value = os.path.getmtime(magic_path)
                            problem.save()
                        else:
                            problem_was_deleted = True
            if not problem_was_deleted:
                response = function(request, id, *args, **kwargs)
                if write:
                    synchronization.export_from_database(Problem.objects.get(id=id))
                return response
            else:
                return render_to_response('problem/deleted_problem.html',
                                          {"path": problem_path})
        return wrapped_function
    return wrapped_decorator
