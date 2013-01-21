from ..models  import Genre
from django.template import RequestContext
from django.shortcuts import render_to_response

def show_genres(request):
    return render_to_response("genres.html",
                    {'nodes':Genre.objects.all()},
                     context_instance=RequestContext(request))