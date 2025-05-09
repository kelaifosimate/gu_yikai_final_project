from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from hashlib import sha1
from django.contrib import messages
from .models import UserInfo
from .user_decorator import login


def register(request):
    context = {
        'title': 'User Registration',
    }
    return render(request, 'fm_user/register.html', context)


def register_handle(request):
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    confirm_pwd = request.POST.get('confirm_pwd')

    if UserInfo.objects.filter(uname=username).exists():
        messages.error(request, "Username already exists.")
        return redirect('/user/register/')

    if password != confirm_pwd:
        messages.error(request, "Passwords do not match.")
        return redirect('/user/register/')

    s1 = sha1()
    s1.update(password.encode('utf8'))
    encrypted_pwd = s1.hexdigest()

    UserInfo.objects.create(
        uname=username,
        upwd=encrypted_pwd,
    )

    messages.success(request, "Registration successful! Please login.")
    return redirect(reverse("fm_user:login"))


def register_exist(request):
    username = request.GET.get('uname')

    count = 0
    if username:
        count = UserInfo.objects.filter(uname=username).count()

    return JsonResponse({'count': count})


def login_view(request):
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

    try:
        user = UserInfo.objects.get(uname=uname)

        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == user.upwd:
            url = request.COOKIES.get('url', '/')
            red = redirect(url)

            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)

            request.session['user_id'] = user.id
            request.session['user_name'] = uname
            return red
    except UserInfo.DoesNotExist:
        from django.contrib.auth import authenticate
        from django.contrib.auth.models import User

        user = authenticate(username=uname, password=upwd)
        if user is not None:
            try:
                user_info = UserInfo.objects.get(uname=uname)
            except UserInfo.DoesNotExist:
                s1 = sha1()
                s1.update(upwd.encode('utf8'))
                encrypted_pwd = s1.hexdigest()

                user_info = UserInfo.objects.create(
                    uname=uname,
                    upwd=encrypted_pwd,
                    uemail=user.email if user.email else None
                )

            url = request.COOKIES.get('url', '/')
            red = redirect(url)

            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)

            request.session['user_id'] = user_info.id
            request.session['user_name'] = uname
            return red

    context = {
        'title': 'User Login',
        'error_name': 1,
        'error_pwd': 0,
        'uname': uname,
        'upwd': upwd,
    }
    return render(request, 'fm_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect(reverse("about"))


@login
def info(request):
    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(id=user_id)

    context = {
        'title': 'User Profile',
        'user': user,
    }
    return render(request, 'fm_user/user_center_info.html', context)


@login
def site(request):
    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(id=user_id)

    if request.method == 'POST':
        user.ushou = request.POST.get('ushou')
        user.uaddress = request.POST.get('uaddress')
        user.uyoubian = request.POST.get('uyoubian')
        user.uphone = request.POST.get('uphone')
        user.save()
        messages.success(request, "Address updated successfully.")

    context = {
        'title': 'Shipping Address',
        'user': user,
    }
    return render(request, 'fm_user/user_center_site.html', context)


@login
def order(request, page_number=1):
    from django.core.paginator import Paginator

    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(id=user_id)

    from apps.fm_order.models import OrderInfo

    orders = OrderInfo.objects.filter(user_id=user_id).order_by('-odate')
    paginator = Paginator(orders, 5)

    try:
        page = paginator.page(page_number)
    except:
        page = paginator.page(1)

    context = {
        'title': 'Order History',
        'user': user,
        'orders': page.object_list,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'fm_user/user_center_order.html', context)