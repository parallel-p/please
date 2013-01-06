from django.shortcuts import render_to_response
from django.template import RequestContext

from problem.forms import tags_edit_form
from problem.models import Problem, ProblemTag
from problem.helpers import problem_sync


@problem_sync(read=True, write=True)
def process_edit_tags(request, id):
    problem = Problem.objects.get(id=id)

    if request.method == 'POST':
        form = tags_edit_form(problem)(request.POST)
        if form.is_valid():
            for to_delete in form.cleaned_data['added_tags']:
                problem.tags.remove(ProblemTag.objects.get(name=to_delete))
            other_tags = form.cleaned_data['other_tags']
            for tag in other_tags:
                if tag:
                    problem.tags.add(ProblemTag.objects.get(name=tag))
            if form.cleaned_data['add_tag']:
                for tag in map(str.strip, form.cleaned_data['add_tag'].split(';')):
                    if tag:
                        problem.tags.add(ProblemTag.objects.get_or_create(name=tag)[0])
            problem.save()

    form = tags_edit_form(problem)()
    return {'form': form, 'id': id, 'any_related_tags': bool(len(problem.tags.all()))}


def edit_tags_view(request, id):
    return render_to_response('tags.html',
                              {'edit_tags': process_edit_tags(request, id)},
                              context_instance=RequestContext(request))
