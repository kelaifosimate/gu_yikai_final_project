from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from hashlib import sha1
from .models import UserInfo
from .forms import UserForm, UserProfileForm
from .user_decorator import login
from apps.fm_order.models import OrderInfo


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Encrypt password
            s1 = sha1()
            s1.update(user.upwd.encode('utf8'))
            user.upwd = s1.hexdigest()

            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('fm_user:login')
    else:
        form = UserForm()

    context = {
        'title': 'Register',
        'form': form,
    }
    return render(request, 'fm_user/register.html', context)


def register_exist(request):
    username = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=username).count()
    return JsonResponse({'count': count})


def login_view(request):
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': 'Login',
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
        else:
            # Password incorrect
            context = {
                'title': 'Login',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
            }
            return render(request, 'fm_user/login.html', context)
    except UserInfo.DoesNotExist:
        context = {
            'title': 'Login',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
        }
        return render(request, 'fm_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('fm_user:login')


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
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect('fm_user:site')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'title': 'Shipping Address',
        'form': form,
        'user': user,
    }
    return render(request, 'fm_user/user_center_site.html', context)


@login
def order(request, page=1):
    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(id=user_id)

    orders = OrderInfo.objects.filter(user_id=user_id).order_by('-odate')

    from django.core.paginator import Paginator
    paginator = Paginator(orders, 5)  # 5 orders per page

    try:
        page_obj = paginator.page(page)
    except:
        page_obj = paginator.page(1)

    context = {
        'title': 'Order History',
        'user': user,
        'orders': page_obj.object_list,
        'page': page_obj,
        'paginator': paginator,
    }

    return render(request, 'fm_user/user_center_order.html', context)