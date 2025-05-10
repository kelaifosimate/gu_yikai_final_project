from django.shortcuts import redirect
from django.urls import reverse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_pages = [
            '/about/',
            '/user/login/',
            '/user/register/',
            '/user/register_handle/',
            '/user/register_exist/',
            '/user/login_handle/',
            '/admin/',
        ]

        if not any(request.path.startswith(page) for page in public_pages):
            if request.user.is_authenticated:
                if 'user_id' not in request.session:
                    request.session['user_id'] = request.user.id
                    request.session['user_name'] = request.user.username
            elif 'user_id' not in request.session:
                if request.path == '/':
                    return redirect(reverse('about'))

                return redirect(reverse('fm_user:login'))

        response = self.get_response(request)
        return response