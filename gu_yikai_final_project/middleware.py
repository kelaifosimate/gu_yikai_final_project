from django.shortcuts import redirect
from django.urls import reverse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Pages accessible without authentication
        public_pages = [
            '/about/',
            '/user/login/',
            '/user/register/',
            '/user/register_handle/',
            '/user/register_exist/',
            '/user/login_handle/',
            '/admin/',
        ]

        # Check if user is authenticated for non-public pages
        if not any(request.path.startswith(page) for page in public_pages):
            if 'user_id' not in request.session:
                # Home page redirects to about
                if request.path == '/':
                    return redirect(reverse('about'))

                # Other pages redirect to login
                return redirect(reverse('fm_user:login'))

        response = self.get_response(request)
        return response