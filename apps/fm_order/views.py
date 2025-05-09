from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import OrderInfo, OrderDetailInfo
from .forms import OrderForm, OrderDetailForm
from apps.fm_cart.models import CartInfo
from apps.fm_user.models import UserInfo
from apps.fm_goods.models import GoodsInfo
from apps.fm_user.user_decorator import login


class OrderList(ListView):
    model = OrderInfo
    template_name = 'fm_order/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        user_id = self.request.session.get('user_id')
        return OrderInfo.objects.filter(user_id=user_id).order_by('-odate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Order History'
        return context


class OrderDetail(DetailView):
    model = OrderInfo
    template_name = 'fm_order/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['title'] = f'Order #{order.oid}'
        context['order_items'] = order.details.all()
        return context


@login
def order_checkout(request):
    """Show checkout page"""
    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    # Get cart items (fresh query to ensure latest data)
    carts = CartInfo.objects.filter(user_id=uid).select_related('goods')
    if not carts.exists():
        messages.warning(request, "Your cart is empty.")
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

    return render(request, 'fm_order/place_order.html', context)


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

        # For non-AJAX requests, redirect to homepage
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            from django.shortcuts import redirect
            messages.success(request, "Order placed successfully!")
            return redirect('fm_goods:index')

        # For AJAX requests, return JSON response
        return JsonResponse({'ok': 1, 'redirect': '/'})

    except Exception as e:
        # Rollback transaction
        transaction.savepoint_rollback(savepoint)
        return JsonResponse({'ok': 0, 'message': str(e)})


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