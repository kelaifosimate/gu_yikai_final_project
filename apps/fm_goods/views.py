from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import GoodsInfo, TypeInfo
from apps.fm_user.models import UserInfo
from apps.fm_cart.models import CartInfo


def index(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first() if username else None

    typelist = TypeInfo.objects.all()

    type0 = typelist[0].goodsinfo_set.order_by('-id')[:4]  # Latest products
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[:4]  # Most popular products

    cart_num = 0
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': 'Home',
        'cart_num': cart_num,
        'guest_cart': 1 if 'user_id' in request.session else 0,
        'type0': type0,
        'type01': type01,
        'user': user,
    }

    return render(request, 'fm_goods/index.html', context)


def detail(request, gid):
    goods = GoodsInfo.objects.get(pk=int(gid))

    goods.gclick = goods.gclick + 1
    goods.save()

    user = None
    if 'user_id' in request.session:
        user = UserInfo.objects.get(id=request.session['user_id'])

    news = goods.gtype.goodsinfo_set.order_by('-id')[:2]

    context = {
        'title': goods.gtype.ttitle,
        'guest_cart': 1 if 'user_id' in request.session else 0,
        'cart_num': get_cart_count(request),
        'goods': goods,
        'news': news,
        'id': gid,
        'user': user,
    }

    return render(request, 'fm_goods/detail.html', context)


def get_cart_count(request):
    if 'user_id' in request.session:
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    return 0