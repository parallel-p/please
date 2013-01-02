from django.shortcuts import render_to_response, redirect
import linux_user


def home(request):
    return render_to_response('home.html', {'user': request.user})


def index(request):
    if request.user.is_authenticated():
        return redirect('/home')
    else:
        return redirect('/login')


def linux_pass(request):
    password = linux_user.pwgen(8)
    print('\x1b[42m' + '-' * 30 + ' password for '
        + request.user.username + ' should be changed here ' +
        '-' * 30 + '\x1b[0m')
    linux_user.set_password(request.user.username, password)
    return render_to_response('linux_pass.html', {'pass': password,
                                                  'user': request.user})
