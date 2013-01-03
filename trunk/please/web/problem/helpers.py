from problem.models import Problem
from problem.synchronization import import_to_database, export_from_database


def problem_sync(read=True, write=False):
    def wrapped_decorator(function):
        def wrapped_function(request, id, *args, **kwargs):
            if read:
                try:
                    problem = Problem.objects.get(id=id)
                except Problem.DoesNotExist:
                    problem = None
                if problem:
                    import_to_database(problem)
                    problem.save()
            response = function(request, id, *args, **kwargs)
            if write:
                export_from_database(Problem.objects.get(id=id))
            return response
        return wrapped_function
    return wrapped_decorator
