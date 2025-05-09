from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
from decimal import Decimal
from .models import OrderInfo, OrderDetailInfo
from apps.fm_cart.models import CartInfo
from apps.fm_user.models import UserInfo
from apps.fm_user import user_decorator


@user_decorator.login
def order(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)

    carts = CartInfo.objects.filter(user_id=uid)

    total_price = 0
    for cart in carts:
        total_price += float(cart.count) * float(cart.goods.gprice)

    total_price = float('%0.2f' % total_price)
    shipping_fee = 10  # Fixed shipping fee
    total_with_shipping = total_price + shipping_fee

    context = {
        'title': 'Checkout',
        'user': user,
        'carts': carts,
        'total_price': total_price,
        'shipping_fee': shipping_fee,
        'total_with_shipping': total_with_shipping,
    }

    return render(request, 'fm_order/place_order.html', context)


@user_decorator.login
@transaction.atomic()
def order_handle(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)

    tran_id = transaction.savepoint()

    try:
        order_info = OrderInfo()
        now = datetime.now()
        order_info.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order_info.odate = now
        order_info.user_id = uid
        order_info.ototal = Decimal(request.POST.get('total'))
        order_info.oaddress = user.uaddress
        order_info.save()

        carts = CartInfo.objects.filter(user_id=uid)

        for cart in carts:
            order_detail = OrderDetailInfo()
            order_detail.order = order_info
            goods = cart.goods

            if cart.count <= goods.gkucun:
                goods.gkucun -= cart.count
                goods.save()

                order_detail.goods = goods
                order_detail.price = goods.gprice
                order_detail.count = cart.count
                order_detail.save()

                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'ok': 0, 'message': 'Insufficient inventory'})

        transaction.savepoint_commit(tran_id)
        return JsonResponse({'ok': 1})

    except Exception as e:
        transaction.savepoint_rollback(tran_id)
        return JsonResponse({'ok': 0, 'message': str(e)})


@user_decorator.login
def order_list(request, page=1):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)

    orders = OrderInfo.objects.filter(user_id=uid).order_by('-odate')

    from django.core.paginator import Paginator
    paginator = Paginator(orders, 10)  # 10 orders per page
    orders_page = paginator.page(page)

    context = {
        'title': 'Order History',
        'user': user,
        'orders': orders_page.object_list,
        'page': orders_page,
        'paginator': paginator,
    }

    return render(request, 'fm_order/order_list.html', context)


@user_decorator.login
def order_detail(request, order_id):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)

    try:
        order = OrderInfo.objects.get(oid=order_id, user_id=uid)
    except OrderInfo.DoesNotExist:
        return redirect('fm_user:order', 1)

    # Get order details
    details = OrderDetailInfo.objects.filter(order=order)

    context = {
        'title': 'Order Details',
        'user': user,
        'order': order,
        'details': details,
    }

    return render(request, 'fm_order/order_detail.html', context)