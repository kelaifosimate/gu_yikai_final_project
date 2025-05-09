from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.fm_user import user_decorator
from .models import CartInfo
from apps.fm_user.models import UserInfo


@user_decorator.login
def user_cart(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    carts = CartInfo.objects.filter(user_id=uid)
    cart_num = carts.count()

    context = {
        'title': 'Shopping Cart',
        'carts': carts,
        'cart_num': cart_num,
        'user': user,
    }

    return render(request, 'fm_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count=1):
    uid = request.session['user_id']
    gid, count = int(gid), int(count)

    try:
        cart = CartInfo.objects.get(user_id=uid, goods_id=gid)
        cart.count += count
    except CartInfo.DoesNotExist:
        cart = CartInfo(user_id=uid, goods_id=gid, count=count)

    cart.save()

    if request.is_ajax():
        cart_num = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count': cart_num})
    else:
        return redirect('fm_cart:cart')


@user_decorator.login
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
    except Exception:
        data = {'ok': 0}

    return JsonResponse(data)