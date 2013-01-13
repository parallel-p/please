import os

from django.shortcuts import render_to_response
from contest.models import Contest
from contest import synchronization


def contest_sync(read=True, write=False):
    def wrapped_decorator(function):
        def wrapped_function(request, id, *args, **kwargs):
            contest_was_deleted = False

            if read:
                try:
                    contest = Contest.objects.get(id=id)
                except Contest.DoesNotExist:
                    contest = None
                contest_path = contest.path if contest else None
                if contest:
                    contest = synchronization.import_to_database(contest)
                    if contest:
                        contest.save()
                    else:
                        contest_was_deleted = True
            if not contest_was_deleted:
                response = function(request, id, *args, **kwargs)
                if write:
                    synchronization.export_from_database(Contest.objects.get(id=id))
                return response
            else:
                return render_to_response('contest/deleted_contest.html',
                                          {"path": contest_path})
        return wrapped_function
    return wrapped_decorator
