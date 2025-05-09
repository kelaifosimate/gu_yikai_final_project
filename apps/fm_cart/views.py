from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CartInfo
from apps.fm_goods.models import GoodsInfo
from apps.fm_user.models import UserInfo
from apps.fm_user.user_decorator import login


@login
def cart(request):
    """Display user's shopping cart"""
    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)
    carts = CartInfo.objects.filter(user_id=uid)

    # Calculate total price
    total_price = 0
    for cart in carts:
        total_price += float(cart.goods.gprice) * cart.count

    context = {
        'title': 'Shopping Cart',
        'user': user,
        'carts': carts,
        'total_price': total_price,
    }

    return render(request, 'fm_cart/cart.html', context)


@login
def add(request, goods_id, count=1):
    """Add item to cart or update quantity"""
    goods_id = int(goods_id)
    count = int(count)

    # Check inventory
    goods = GoodsInfo.objects.get(id=goods_id)
    if count > goods.gkucun:
        return JsonResponse({'ok': 0, 'message': 'Insufficient inventory'})

    # Get user cart item or create new one
    uid = request.session.get('user_id')
    try:
        cart_item = CartInfo.objects.get(user_id=uid, goods_id=goods_id)
        cart_item.count += count
    except CartInfo.DoesNotExist:
        cart_item = CartInfo(user_id=uid, goods_id=goods_id, count=count)

    cart_item.save()

    # Return cart count for AJAX requests
    if request.is_ajax():
        cart_count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'ok': 1, 'count': cart_count})

    # Redirect to cart for normal requests
    return redirect('fm_cart:cart')


@login
def update(request, cart_id, count):
    """Update item quantity in cart"""
    cart_id = int(cart_id)
    count = int(count)

    try:
        cart_item = CartInfo.objects.get(id=cart_id)

        # Check inventory
        if count > cart_item.goods.gkucun:
            count = cart_item.goods.gkucun

        # Update count
        cart_item.count = count
        cart_item.save()

        # Calculate new subtotal
        subtotal = float(cart_item.goods.gprice) * count

        # Calculate new total
        uid = request.session.get('user_id')
        carts = CartInfo.objects.filter(user_id=uid)
        total = sum(float(item.goods.gprice) * item.count for item in carts)

        return JsonResponse({
            'ok': 1,
            'subtotal': subtotal,
            'total': total,
        })
    except CartInfo.DoesNotExist:
        return JsonResponse({'ok': 0})


@login
def delete(request, cart_id):
    """Delete item from cart"""
    cart_id = int(cart_id)

    try:
        cart_item = CartInfo.objects.get(id=cart_id)
        cart_item.delete()

        # Calculate new total
        uid = request.session.get('user_id')
        carts = CartInfo.objects.filter(user_id=uid)
        total = sum(float(item.goods.gprice) * item.count for item in carts)

        return JsonResponse({
            'ok': 1,
            'total': total,
            'count': carts.count(),
        })
    except CartInfo.DoesNotExist:
        return JsonResponse({'ok': 0})