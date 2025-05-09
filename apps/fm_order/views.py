from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from decimal import Decimal
from .models import OrderInfo, OrderDetailInfo
from apps.fm_cart.models import CartInfo
from apps.fm_user.models import UserInfo
from apps.fm_goods.models import GoodsInfo
from apps.fm_user.user_decorator import login


@login
def order(request):
    """Show checkout page"""
    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    # Get cart items
    carts = CartInfo.objects.filter(user_id=uid)
    if not carts.exists():
        return redirect('fm_cart:cart')

    # Calculate totals
    total_price = sum(float(cart.goods.gprice) * cart.count for cart in carts)
    shipping_fee = 10.00  # Fixed shipping fee
    total_with_shipping = total_price + shipping_fee

    context = {
        'title': 'Checkout',
        'user': user,
        'carts': carts,
        'total_price': total_price,
        'shipping_fee': shipping_fee,
        'total_with_shipping': total_with_shipping,
    }

    return render(request, 'fm_order/order.html', context)


@login
@transaction.atomic
def order_handle(request):
    """Process order submission"""
    if request.method != 'POST':
        return JsonResponse({'ok': 0, 'message': 'Invalid request method'})

    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    # Check if user has shipping info
    if not user.ushou or not user.uaddress or not user.uphone:
        return JsonResponse({'ok': 0, 'message': 'Please complete your shipping information'})

    # Get cart items
    carts = CartInfo.objects.filter(user_id=uid)
    if not carts.exists():
        return JsonResponse({'ok': 0, 'message': 'Your cart is empty'})

    # Create transaction savepoint
    savepoint = transaction.savepoint()

    try:
        # Create order
        order = OrderInfo()
        order.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(uid)
        order.user = user
        order.odate = datetime.now()
        order.ototal = Decimal(request.POST.get('total', '0'))
        order.oaddress = user.uaddress
        order.save()

        # Create order items
        for cart in carts:
            # Check inventory
            if cart.count > cart.goods.gkucun:
                transaction.savepoint_rollback(savepoint)
                return JsonResponse({'ok': 0, 'message': f'Insufficient inventory for {cart.goods.gtitle}'})

            # Update inventory
            cart.goods.gkucun -= cart.count
            cart.goods.save()

            # Create order detail
            detail = OrderDetailInfo()
            detail.order = order
            detail.goods = cart.goods
            detail.price = cart.goods.gprice
            detail.count = cart.count
            detail.save()

            # Delete cart item
            cart.delete()

        # Commit transaction
        transaction.savepoint_commit(savepoint)
        return JsonResponse({'ok': 1})

    except Exception as e:
        # Rollback transaction
        transaction.savepoint_rollback(savepoint)
        return JsonResponse({'ok': 0, 'message': str(e)})


@login
def order_list(request, page=1):
    """Show order history"""
    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    # Get orders
    orders = OrderInfo.objects.filter(user_id=uid).order_by('-odate')

    # Paginate
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

    return render(request, 'fm_order/order_list.html', context)


@login
def order_detail(request, order_id):
    """Show order details"""
    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    # Get order
    order = get_object_or_404(OrderInfo, oid=order_id, user_id=uid)

    # Get order items
    order_items = OrderDetailInfo.objects.filter(order=order)

    context = {
        'title': 'Order Details',
        'user': user,
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'fm_order/order_detail.html', context)


@login
def pay(request, order_id):
    """Process payment"""
    if request.method != 'POST':
        return JsonResponse({'ok': 0, 'message': 'Invalid request method'})

    uid = request.session.get('user_id')

    # Get order
    try:
        order = OrderInfo.objects.get(oid=order_id, user_id=uid)

        # Update order status
        order.oIsPay = True
        order.save()

        return JsonResponse({'ok': 1})
    except OrderInfo.DoesNotExist:
        return JsonResponse({'ok': 0, 'message': 'Order not found'})