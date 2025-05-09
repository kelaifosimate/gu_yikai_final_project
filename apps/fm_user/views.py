from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse

from hashlib import sha1
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import UserInfo


def register(request):
    context = {
        'title': 'User Registration',
    }
    return render(request, 'fm_user/register.html', context)


def register_handle(request):
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    confirm_pwd = request.POST.get('confirm_pwd')
    email = request.POST.get('email')

    # Validate password consistency
    if password != confirm_pwd:
        messages.error(request, "Passwords do not match.")
        return redirect('/user/register/')

    # Password encryption
    s1 = sha1()
    s1.update(password.encode('utf8'))
    encrypted_pwd = s1.hexdigest()

    # Create object
    UserInfo.objects.create(uname=username, upwd=encrypted_pwd, uemail=email)

    # Registration success
    messages.success(request, "Registration successful! Please login.")
    return redirect(reverse("fm_user:login"))


def register_exist(request):
    username = request.GET.get('uname')
    uemail = request.GET.get('uemail')
    count = UserInfo.objects.filter(uname=username).count()
    email_count = UserInfo.objects.filter(uemail=uemail).count()
    return JsonResponse({'count': count, 'email_count': email_count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': 'User Login',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
    }
    return render(request, 'fm_user/login.html', context)


def login_handle(request):
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    jizhu = request.POST.get('jizhu', 0)
    user = UserInfo.objects.filter(uname=uname)

    if len(user) == 1:  # Validate user password and redirect
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == user[0].upwd:
            url = request.COOKIES.get('url', '/')
            red = redirect(url)

            # Whether to remember username (set cookie)
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)  # Set expiry cookie time, expire immediately

            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {
                'title': 'User Login',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
            }
            return render(request, 'fm_user/login.html', context)
    else:
        context = {
            'title': 'User Login',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
        }
        return render(request, 'fm_user/login.html', context)


def logout(request):
    request.session.flush()  # Clear all current user sessions
    return redirect(reverse("fm_goods:index"))


def info(request):
    """User profile page - simplified version matching EZ University style"""
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(reverse("fm_user:login"))

    user = UserInfo.objects.get(id=user_id)
    context = {
        'title': 'User Profile',
        'user': user,
    }
    return render(request, 'fm_user/user_center_info.html', context)


# Keep minimal basic functionality for other pages that might be referenced
def order(request, page_number):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(reverse("fm_user:login"))

    context = {
        'title': 'Orders',
        'page': {'number': page_number},
    }
    return render(request, 'fm_user/user_center_order.html', context)


def site(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(reverse("fm_user:login"))

    user = UserInfo.objects.get(id=user_id)

    if request.method == 'POST':
        user.ushou = request.POST.get('ushou')
        user.uphone = request.POST.get('uphone')
        user.uyoubian = request.POST.get('uyoubian')
        user.uaddress = request.POST.get('uaddress')
        user.save()
        messages.success(request, "Address updated successfully.")

    context = {
        'title': 'Shipping Address',
        'user': user,
    }
    return render(request, 'fm_user/user_center_site.html', context)