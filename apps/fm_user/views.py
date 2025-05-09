import uuid
from random import Random
from datetime import datetime

from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q  # 添加 Q 查询对象

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
    return render(request, 'register.html', context)


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
    return render(request, 'login.html', context)


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
    return render(request, 'login.html', context)


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
            return render(request, 'login.html', context)
        else:
            context = {
                'title': 'User Login',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
                'user': user,
            }
            return render(request, 'login.html', context)
    else:
        context = {
            'title': 'User Login',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
            'user': user,
        }
        return render(request, 'login.html', context)


def logout(request):  # 用户登出
    request.session.flush()  # 清空当前用户所有session
    return redirect(reverse("fm_goods:index"))


@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail

    # 获取最近浏览信息
    goods_list = []
    goods_ids = GoodsBrowser.objects.filter(user_id=request.session['user_id']).order_by("-browser_time")

    for goods_id in goods_ids:
        goods_list.append(GoodsInfo.objects.get(id=goods_id.good_id))

    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    context = {
        'title': 'User Center',
        'user_email': user_email,
        'user': user,
        'goods_list': goods_list,
    }

    return render(request, 'user_center_info.html', context)


@user_decorator.login
def order(request, pindex):
    user_id = request.session['user_id']
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by('-oid')
    tuohuo_infos = ReturnInfo.objects.filter()
    paginator = Paginator(orders_list, 2)

    if pindex == '':
        pindex = '1'

    page = paginator.page(int(pindex))

    context = {
        'paginator': paginator,
        'page': page,
        'user': user,
        'tuohuo_infos': tuohuo_infos,
    }

    return render(request, 'user_center_order.html', context)


@user_decorator.login
def site(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    if request.method == "POST":
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()

    context = {'title': 'User Center', 'user': user}
    return render(request, 'user_center_site.html', context)


@user_decorator.login
def publishers(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    typeinfos = TypeInfo.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        jianjie = request.POST.get('jianjie')
        price = request.POST.get('price')
        unit = user.uname
        content = request.POST.get('content')
        pic = request.FILES.get('pic')
        kucun = request.POST.get('kucun')
        type_id = request.POST.get('type_id')

        if pic:
            # 创建商品
            goods = GoodsInfo()
            goods.gtitle = title
            goods.gprice = price
            goods.gunit = unit
            goods.gjianjie = jianjie
            goods.gkucun = kucun
            goods.gcontent = content
            goods.gpic = pic
            goods.gtype_id = type_id
            goods.save()
            messages.success(request, "Item listed successfully")
        else:
            messages.error(request, "Please upload an image")

    context = {
        'title': 'List Item',
        'user': user,
        'typeinfos': typeinfos,
    }
    return render(request, 'user_publishers.html', context)


@user_decorator.login
def changeInformation(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    if request.method == "POST":
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        personinf = request.POST.get('personinf')
        logo = request.FILES.get('logo')

        user.usex = sex
        user.uage = age
        user.upersonInf = personinf

        if logo:
            user.ulogo = logo

        user.save()
        messages.success(request, "Profile updated successfully")

    context = {
        'title': 'Edit Profile',
        'user': user,
    }
    return render(request, 'user_changeInformation.html', context)


@user_decorator.login
def check_user(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    if request.method == "POST":
        name = request.POST.get('name')
        type_id = request.POST.get('type_id')
        tel = request.POST.get('tel')
        pic = request.FILES.get('pic')

        user.urealname = name
        user.uzhengjian_type = type_id
        user.uzhengjian_tel = tel

        if pic:
            user.uzhengjian_img = pic

        user.save()
        messages.success(request, "ID verification submitted successfully")

    context = {
        'title': 'ID Verification',
        'user': user,
    }
    return render(request, 'user_check_username.html', context)


@user_decorator.login
def myself_information(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    # 获取用户发布的商品
    goods = GoodsInfo.objects.filter(gunit=username)

    # 获取用户的订单
    orderinfs = OrderDetailInfo.objects.filter(shopername=username)

    # 获取商品信息
    infors = GoodsInfo.objects.all()

    context = {
        'user': user,
        'goods': goods,
        'orderinfs': orderinfs,
        'infors': infors,
    }
    return render(request, 'myself_information.html', context)


@user_decorator.login
def seller_information(request, sellername):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    # 获取卖家信息
    shoper = UserInfo.objects.filter(uname=sellername).first()

    # 获取卖家发布的商品
    goods = GoodsInfo.objects.filter(gunit=sellername)

    # 获取卖家的订单
    orderinfs = OrderDetailInfo.objects.filter(shopername=sellername)

    # 获取商品信息
    infos = GoodsInfo.objects.all()

    # 处理消息发送
    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('Message')

        # 创建消息
        info = Information()
        info.ctitle = title
        info.cusername = username
        info.cusername1 = sellername
        info.ccontent_chart = message
        info.cinformation_id = shoper.id
        info.save()

        messages.success(request, "Message sent successfully")

    context = {
        'user': user,
        'shoper': shoper,
        'goods': goods,
        'orderinfs': orderinfs,
        'infos': infos,
        'Content': {'cusername': sellername},
    }
    return render(request, 'shoper_information.html', context)


@user_decorator.login
def message(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    # 获取所有消息
    persons = Information.objects.filter(cusername1=username).values('cusername').distinct()

    # 获取所有用户信息
    imgs = UserInfo.objects.all()

    context = {
        'title': 'Message Center',
        'user': user,
        'persons': persons,
        'imgs': imgs,
    }
    return render(request, 'user_messages.html', context)


@user_decorator.login
def person_message(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    # 获取特定用户的消息
    message_username = request.GET.get('username')

    # 标记消息为已读
    Information.objects.filter(cusername=message_username, cusername1=username).update(ccheck=True)

    # 获取所有相关消息
    informations = Information.objects.filter(
        (Q(cusername=message_username) & Q(cusername1=username)) |
        (Q(cusername=username) & Q(cusername1=message_username))
    ).order_by('date_publish')

    # 获取所有消息人
    persons = Information.objects.filter(cusername1=username).values('cusername').distinct()

    # 获取所有用户信息
    imgs = UserInfo.objects.all()

    # 获取消息用户的头像
    logo = UserInfo.objects.filter(uname=message_username).first()

    # 处理发送消息
    if request.method == "POST":
        content = request.POST.get('title')
        receiver = UserInfo.objects.filter(uname=message_username).first()

        if content:
            Information.objects.create(
                ctitle=content,
                cusername=username,
                cusername1=message_username,
                ccontent_chart=content,
                cinformation_id=receiver.id
            )
            messages.success(request, "Message sent successfully")
        else:
            messages.error(request, "Message cannot be empty")

    context = {
        'title': 'Message Details',
        'user': user,
        'username': message_username,
        'informations': informations,
        'persons': persons,
        'imgs': imgs,
        'logo': logo,
    }
    return render(request, 'user_messages.html', context)


@user_decorator.login
def changeInPwd(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    if request.method == "POST":
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match")
        else:
            # 密码加密
            s1 = sha1()
            s1.update(password.encode('utf8'))
            encrypted_pwd = s1.hexdigest()

            user.upwd = encrypted_pwd
            user.save()
            messages.success(request, "Password changed successfully")

    context = {
        'title': 'Change Password',
        'user': user,
    }
    return render(request, 'user_changePwd.html', context)


def findpwdView(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')

        if username and email:
            user = UserInfo.objects.filter(uname=username, uemail=email).first()
            if user:
                # 生成随机密码
                password = ''.join(Random().sample('abcdefghijklmnopqrstuvwxyz0123456789', 8))

                # 发送邮件
                subject = 'Password Reset'
                message = f'Your new password is: {password}'
                from_email = 'fleamarket@example.com'
                recipient_list = [email]

                try:
                    send_mail(subject, message, from_email, recipient_list)

                    # 更新密码
                    s1 = sha1()
                    s1.update(password.encode('utf8'))
                    encrypted_pwd = s1.hexdigest()

                    user.upwd = encrypted_pwd
                    user.save()

                    messages.success(request, "Password reset email sent")
                    return redirect('fm_user:login')
                except Exception as e:
                    messages.error(request, f"Error sending email: {e}")
            else:
                messages.error(request, "Username and email do not match")
        else:
            messages.error(request, "Please provide both username and email")

    return render(request, 'change_password1.html', {'title': 'Reset Password'})


@user_decorator.login
def return_item(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()

    if request.method == "POST":
        title = request.POST.get('title')
        username1 = request.POST.get('username')
        username2 = request.POST.get('username1')
        person_number = request.POST.get('person_number')
        order_number = request.POST.get('order_number')
        kuaidi = request.POST.get('kuaidi')
        kuaidi_number = request.POST.get('kuaidi_number')
        address = request.POST.get('address')
        address1 = request.POST.get('address1')
        text = request.POST.get('text')

        # 创建退货信息
        ReturnInfo.objects.create(
            title=title,
            username=username1,
            username1=username2,
            person_number=person_number,
            order_number=order_number,
            kuaidi=kuaidi,
            kuaidi_number=kuaidi_number,
            address=address,
            address1=address1,
            text=text
        )

        messages.success(request, "Return request submitted successfully")
        return redirect('fm_user:order', 1)

    context = {
        'title': 'Return Item',
        'user': user,
    }
    return render(request, 'tuihuo.html', context)