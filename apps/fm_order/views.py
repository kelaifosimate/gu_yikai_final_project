from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse

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
    cart_ids = request.GET.getlist('cart_id')
    carts = []
    total_price = 0
    for goods_id in cart_ids:
        cart = CartInfo.objects.get(id=goods_id)
        carts.append(cart)
        total_price = total_price + float(cart.count) * float(cart.goods.gprice)

    total_price = float('%0.2f' % total_price)
    trans_cost = 10  # Shipping fee
    total_trans_price = trans_cost + total_price
    context = {
        'title': 'Submit Order',
        'page_name': 1,
        'user': user,
        'carts': carts,
        'total_price': float('%0.2f' % total_price),
        'trans_cost': trans_cost,
        'total_trans_price': total_trans_price,
    }
    return render(request, 'fm_order/place_order.html', context)

'''
Transaction submission:
Any step that goes wrong in these steps will roll back the entire process
1. Create order object
2. Check if product inventory is sufficient
3. Create order details, multiple ones
4. Modify product inventory
5. Delete from shopping cart
'''


@user_decorator.login
@transaction.atomic()  # Transaction
def order_handle(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    tran_id = transaction.savepoint()  # Save transaction point
    cart_ids = request.POST.get('cart_ids')  # Order cart submitted by user, at this time cart_ids is a string, e.g., '1,2,3,'
    user_id = request.session['user_id']  # Get current user's id
    data = {}
    try:
        order_info = OrderInfo()  # Create an order object
        now = datetime.now()
        order_info.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id)  # Order number is a concatenation of order submission time and user id
        order_info.odate = now  # Order time
        order_info.user_id = int(user_id)  # User id of the order
        order_info.ototal = Decimal(request.POST.get('total'))  # Order total price from frontend
        order_info.oaddress = user.uaddress
        order_info.save()  # Save order

        for cart_id in cart_ids.split(','):  # Process each type of product in the user's submitted order, i.e., each small shopping cart
            cart = CartInfo.objects.get(pk=cart_id)  # Get small shopping cart object from CartInfo table
            order_detail = OrderDetailInfo()  # Each small product order in the main order
            order_detail.order = order_info  # Foreign key relationship, binding small order with main order
            goods = cart.goods  # Specific product
            if cart.count <= goods.gkucun:  # Check if inventory meets the order, if yes, modify database
                goods.gkucun = goods.gkucun - cart.count
                goods.save()
                order_detail.goods = goods
                order_detail.price = goods.gprice
                order_detail.count = cart.count
                order_detail.username = user.uname
                order_detail.shopername = goods.gunit
                order_detail.save()
                cart.delete()  # Delete current shopping cart
            else:  # Otherwise, roll back transaction, cancel order
                transaction.savepoint_rollback(tran_id)
                return HttpResponse('Insufficient inventory')
        data['ok'] = 1
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print("%s" % e)
        print('Order submission incomplete')
        transaction.savepoint_rollback(tran_id)  # If any step in the transaction goes wrong, the entire transaction is cancelled
    return JsonResponse(data)


@user_decorator.login
def pay(request):
    pass