from django.shortcuts import render_to_response
from django.template import RequestContext

from problem.forms import tags_edit_form
from problem.models import Problem, ProblemTag
from problem.helpers import problem_sync


@problem_sync(read=True, write=True)
def process_edit_tags(request, id):
    problem = Problem.objects.get(id=id)

    if request.method == 'POST':
        formclass = tags_edit_form(problem)
        form = formclass(request.POST)
        if form.is_valid():
            problem.tags.clear()
            if not hasattr(formclass, 'added_tags'):
                for to_add in form.cleaned_data['added_tags']:
                    problem.tags.add(ProblemTag.objects.get(name=to_add))
            if not hasattr(formclass, 'other_tags'):
                other_tags = form.cleaned_data['other_tags']
                for tag in other_tags:
                    if tag:
                        problem.tags.add(ProblemTag.objects.get(name=tag))
            if form.cleaned_data['add_tag']:
                for tags in form.cleaned_data['add_tag'].split(';'):
                    for tag in map(str.strip, tags.split(',')):
                        if tag:
                            problem.tags.add(ProblemTag.objects.get_or_create(name=tag)[0])
            problem.save()

    form = tags_edit_form(problem)()
    return {'form': form, 'id': id, 'any_related_tags': bool(len(problem.tags.all()))}


def edit_tags_view(request, id):
    return render_to_response('tags.html',
                              {'edit_tags': process_edit_tags(request, id)},
                              context_instance=RequestContext(request))
