from django.shortcuts import render_to_response, redirect
# from django.contrib import auth


def home(request):
    return render_to_response('home.html', {'user': request.user})


def index(request):
    if request.user.is_authenticated():
        return redirect('/home')
    else:
        return redirect('/login')
