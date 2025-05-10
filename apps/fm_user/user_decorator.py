from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def login(func):
    def login_func(request, *args, **kwargs):
        if 'user_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            if request.path == '/':
                return HttpResponseRedirect(reverse('about'))

            red = HttpResponseRedirect(reverse('fm_user:login'))
            red.set_cookie('url', request.get_full_path())
            return red

    return login_func