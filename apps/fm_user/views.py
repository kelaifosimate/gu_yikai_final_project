import uuid
from random import Random

from django.shortcuts import render, render_to_response
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse

from hashlib import sha1

from django.contrib import messages

import apps.fm_goods
from apps.fm_goods.models import TypeInfo, GoodsInfo, GoodsContent, ContentChart
from apps.fm_cart.models import CartInfo
from .models import GoodsBrowser, UserInfo, Information, ReturnInfo
from . import user_decorator
from apps.fm_order.models import *

from django.core.mail import send_mail


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

    # 验证密码一致性
    if password != confirm_pwd:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(password.encode('utf8'))
    encrypted_pwd = s1.hexdigest()

    # 创建对象
    UserInfo.objects.create(uname=username, upwd=encrypted_pwd, uemail=email)
    # 注册成功
    context = {
        'title': 'User Login',
        'username': username,
    }
    return render(request, 'fm_user/login.html', context)


def register_exist(request):
    username = request.GET.get('uname')
    uemail = request.GET.get('uemail')
    count = UserInfo.objects.filter(uname=username).count()
    email_count = UserInfo.objects.filter(uemail=uemail).count()
    print(email_count)
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


def login_handle(request):  # 没有使用ajax提交表单
    # 接收请求信息
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    jizhu = request.POST.get('jizhu', 0)
    user = UserInfo.objects.filter(uname=uname)
    print("user:%s" % (user))
    if len(user) == 1:  # 判断用户密码并跳转
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == user[0].upwd and user[0].uname_passOrfail == True:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)  # 继承与HttpResponse 在跳转的同时 设置一个cookie值
            # 是否勾选记住用户名，设置cookie
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)  # 设置过期cookie时间，立刻过期
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return red
        elif user[0].uname_passOrfail == False:
            messages.success(request, "Your account has been banned due to violations.")
            context = {
                'title': 'User Login',
                'uname': uname,
                'upwd': upwd,
                'user': user,
            }
            return render(request, 'fm_user/login.html', context)
        else:
            context = {
                'title': 'User Login',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
                'user': user,
            }
            return render(request, 'fm_user/login.html', context)
    else:
        context = {
            'title': 'User Login',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
            'user': user,
        }
        return render(request, 'fm_user/login.html', context)


def logout(request):  # 用户登出
    request.session.flush()  # 清空当前用户所有session
    return redirect(reverse("fm_goods:index"))

# ... 其余代码保持不变 ...