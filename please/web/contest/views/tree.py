from ..models  import Category
from django.template import RequestContext
from django.shortcuts import render_to_response

def show_categories(request):
    return render_to_response("contests/categories.html",
                    {'nodes':Category.objects.all()},
                     context_instance=RequestContext(request))