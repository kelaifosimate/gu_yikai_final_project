from django.http import HttpResponseRedirect
from django.shortcuts import reverse


# If not logged in, redirect to login page
def login(func):
    def login_fun(request, *args, **kwargs):
        if 'user_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect(reverse("fm_user:login"))
            red.set_cookie('url', request.get_full_path())
            # Ensure user can return to the desired page after login verification
            return red
    return login_fun