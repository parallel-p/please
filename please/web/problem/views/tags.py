from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from problem.forms import TagsEditForm

from problem.models import Problem


def process_edit_tags(request, id):
    problem = Problem.objects.get(id=id)
    if request.method == 'POST':
        form = TagsEditForm(request.POST)
        if form.is_valid():
            problem.tags = form.cleaned_data["tags"]
            problem.save()
    else:
        form = TagsEditForm()

    return {'form': form, 'id': id}


def edit_tags_view(request, id):
    return render_to_response('tags.html',
                              {'edit_tags': process_edit_tags(request, id)},
                              context_instance=RequestContext(request))
