from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def login(func):
    def login_func(request, *args, **kwargs):
        if 'user_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            # Redirect to about page for non-logged in users
            if request.path == '/':
                return HttpResponseRedirect(reverse('about'))

            # For other pages, redirect to login with return url
            red = HttpResponseRedirect(reverse('fm_user:login'))
            red.set_cookie('url', request.get_full_path())
            return red

    return login_func