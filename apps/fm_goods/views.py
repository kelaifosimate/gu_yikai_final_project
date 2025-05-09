from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import GoodsInfo
from .forms import GoodsForm
from apps.fm_user.models import UserInfo
from apps.fm_user.user_decorator import login
from apps.fm_cart.models import CartInfo


class ProductList(ListView):
    model = GoodsInfo
    template_name = 'fm_goods/list.html'
    context_object_name = 'goods_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products'
        return context


class ProductDetail(DetailView):
    model = GoodsInfo
    template_name = 'fm_goods/detail.html'
    context_object_name = 'goods'
    pk_url_kwarg = 'goods_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goods = self.get_object()
        context['title'] = goods.gtitle

        # Increment view count
        goods.gclick += 1
        goods.save()

        # Get recommendations
        context['recommended'] = GoodsInfo.objects.exclude(id=goods.id).order_by('-gclick')[:5]

        return context


@login
def add_product(request):
    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.gunit = request.session.get('user_name')
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('fm_goods:detail', goods_id=product.id)
    else:
        form = GoodsForm()

    context = {
        'title': 'Add Product',
        'form': form,
    }
    return render(request, 'fm_goods/add_product.html', context)


@login
def add_product_handle(request):
    if request.method != 'POST':
        return redirect('fm_goods:index')

    form = GoodsForm(request.POST, request.FILES)
    if form.is_valid():
        product = form.save(commit=False)
        product.gunit = request.session.get('user_name')
        product.save()
        messages.success(request, "Product added successfully.")
        return redirect('fm_goods:detail', goods_id=product.id)
    else:
        messages.error(request, "Error adding product. Please check the form.")
        context = {
            'title': 'Add Product',
            'form': form,
        }
        return render(request, 'fm_goods/add_product.html', context)


@login
def edit_product(request, goods_id):
    product = get_object_or_404(GoodsInfo, id=goods_id)

    # Check if current user is the seller
    user_name = request.session.get('user_name')
    if product.gunit != user_name:
        return HttpResponseForbidden("You do not have permission to edit this product.")

    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('fm_goods:detail', goods_id=product.id)
    else:
        form = GoodsForm(instance=product)

    context = {
        'title': 'Edit Product',
        'form': form,
        'product': product,
    }
    return render(request, 'fm_goods/edit_product.html', context)


@login
def edit_product_handle(request, goods_id):
    """Handle edit product form submission"""
    product = get_object_or_404(GoodsInfo, id=goods_id)

    # Check if current user is the seller
    user_name = request.session.get('user_name')
    if product.gunit != user_name:
        return HttpResponseForbidden("You do not have permission to edit this product.")

    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('fm_goods:detail', goods_id=product.id)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('fm_goods:edit_product', goods_id=product.id)


@login
def delete_product(request, goods_id):
    product = get_object_or_404(GoodsInfo, id=goods_id)

    # Check if current user is the seller
    user_name = request.session.get('user_name')
    if product.gunit != user_name:
        return HttpResponseForbidden("You do not have permission to delete this product.")

    context = {
        'title': 'Delete Product',
        'product': product,
    }
    return render(request, 'fm_goods/delete_product.html', context)


@login
def delete_product_handle(request, goods_id):
    """Handle delete product confirmation"""
    product = get_object_or_404(GoodsInfo, id=goods_id)

    # Check if current user is the seller
    user_name = request.session.get('user_name')
    if product.gunit != user_name:
        return HttpResponseForbidden("You do not have permission to delete this product.")

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('fm_goods:list')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('fm_goods:delete_product', goods_id=product.id)


def search(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    if query:
        results = GoodsInfo.objects.filter(
            Q(gtitle__icontains=query) |
            Q(gjianjie__icontains=query)
        )
    else:
        results = GoodsInfo.objects.all()

    paginator = Paginator(results, 10)
    page_obj = paginator.get_page(page)

    context = {
        'title': 'Search Results',
        'query': query,
        'page': page_obj,
        'paginator': paginator,
    }

    return render(request, 'fm_goods/search.html', context)


def index(request):
    # Get newest products
    newest_products = GoodsInfo.objects.order_by('-id')[:8]

    # Get most popular products
    popular_products = GoodsInfo.objects.order_by('-gclick')[:8]

    context = {
        'title': 'Home',
        'newest_products': newest_products,
        'popular_products': popular_products,
    }

    return render(request, 'fm_goods/index.html', context)