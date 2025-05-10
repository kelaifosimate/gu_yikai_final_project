from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth.models import User

def login(func):
    def login_func(request, *args, **kwargs):
        if 'user_id' in request.session:
            return func(request, *args, **kwargs)
        elif request.user.is_authenticated:
            user_id = request.user.id
            request.session['user_id'] = user_id
            request.session['user_name'] = request.user.username
            return func(request, *args, **kwargs)
        else:
            if request.path == '/':
                return HttpResponseRedirect(reverse('about'))

            red = HttpResponseRedirect(reverse('fm_user:login'))
            red.set_cookie('url', request.get_full_path())
            return red

    return login_func