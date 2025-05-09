from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import GoodsInfo, TypeInfo
from apps.fm_cart.models import CartInfo
from apps.fm_user.models import UserInfo
from apps.fm_user.user_decorator import login


def index(request):
    # Redirect to about page for non-logged in users
    if 'user_id' not in request.session:
        return redirect('about')

    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first() if username else None

    typelist = TypeInfo.objects.all()

    # Get new products (latest products)
    type0 = GoodsInfo.objects.order_by('-id')[:8]

    # Get popular products (most clicked)
    type01 = GoodsInfo.objects.order_by('-gclick')[:8]

    # Get cart count
    cart_num = 0
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': 'Home',
        'cart_num': cart_num,
        'type0': type0,
        'type01': type01,
        'user': user,
    }

    return render(request, 'fm_goods/index.html', context)


@login
def list(request, type_id, page_index, sort):
    """Product list view with pagination and sorting"""
    typeinfo = TypeInfo.objects.get(id=int(type_id))

    # Get product list with sorting
    if sort == '1':  # Default sorting (by id)
        goods_list = GoodsInfo.objects.filter(gtype_id=int(type_id)).order_by('-id')
    elif sort == '2':  # Sort by price
        goods_list = GoodsInfo.objects.filter(gtype_id=int(type_id)).order_by('gprice')
    elif sort == '3':  # Sort by popularity
        goods_list = GoodsInfo.objects.filter(gtype_id=int(type_id)).order_by('-gclick')
    else:
        goods_list = GoodsInfo.objects.filter(gtype_id=int(type_id)).order_by('-id')

    # Paginate results
    paginator = Paginator(goods_list, 10)  # 10 items per page

    try:
        page = paginator.page(int(page_index))
    except:
        page = paginator.page(1)

    # Get recommendations (new products)
    news = GoodsInfo.objects.order_by('-id')[:2]

    # Get cart count
    cart_num = 0
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': typeinfo.ttitle,
        'typeinfo': typeinfo,
        'page': page,
        'paginator': paginator,
        'sort': sort,
        'news': news,
        'cart_num': cart_num,
    }

    return render(request, 'fm_goods/list.html', context)


@login
def detail(request, goods_id):
    """Product detail view"""
    goods = GoodsInfo.objects.get(id=int(goods_id))

    # Increment click count
    goods.gclick += 1
    goods.save()

    # Get recommendations (new products in same category)
    news = goods.gtype.goodsinfo_set.order_by('-id')[:2]

    # Get cart count
    cart_num = 0
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': goods.gtitle,
        'goods': goods,
        'news': news,
        'cart_num': cart_num,
    }

    return render(request, 'fm_goods/detail.html', context)


def search(request):
    """Search products view"""
    query = request.GET.get('q', '')
    page_index = request.GET.get('page', '1')

    if query:
        goods_list = GoodsInfo.objects.filter(gtitle__contains=query)
        search_status = 1 if goods_list.exists() else 0
    else:
        goods_list = GoodsInfo.objects.order_by('-id')
        search_status = 1

    # Paginate results
    paginator = Paginator(goods_list, 10)  # 10 items per page

    try:
        page = paginator.page(int(page_index))
    except:
        page = paginator.page(1)

    # Get cart count
    cart_num = 0
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': 'Search Results: ' + query,
        'query': query,
        'page': page,
        'paginator': paginator,
        'search_status': search_status,
        'cart_num': cart_num,
    }

    return render(request, 'fm_goods/search.html', context)


@login
def add_product(request, type_id):
    try:
        typeinfo = TypeInfo.objects.get(id=type_id)
    except TypeInfo.DoesNotExist:
        return redirect('fm_goods:index')

    context = {
        'title': 'Add Product',
        'type_id': type_id,
        'typeinfo': typeinfo,
    }

    return render(request, 'fm_goods/add_product.html', context)


@login
def add_product_handle(request):
    if request.method != 'POST':
        return redirect('fm_goods:index')

    type_id = request.POST.get('type_id')
    gtitle = request.POST.get('gtitle')
    gprice = request.POST.get('gprice')
    gkucun = request.POST.get('gkucun')
    gjianjie = request.POST.get('gjianjie')
    gcontent = request.POST.get('gcontent')
    gpic = request.FILES.get('gpic')

    user_name = request.session.get('user_name')

    try:
        typeinfo = TypeInfo.objects.get(id=type_id)

        product = GoodsInfo.objects.create(
            gtitle=gtitle,
            gprice=gprice,
            gkucun=gkucun,
            gjianjie=gjianjie,
            gcontent=gcontent,
            gpic=gpic,
            gunit=user_name,
            gtype=typeinfo
        )

        messages.success(request, "Product added successfully.")
        return redirect('fm_goods:list', type_id=type_id, page_index=1, sort=1)
    except Exception as e:
        messages.error(request, f"Error adding product: {str(e)}")
        return redirect('fm_goods:add_product', type_id=type_id)


@login
def edit_product(request, goods_id):
    product = get_object_or_404(GoodsInfo, id=goods_id)

    user_name = request.session.get('user_name')
    if product.gunit != user_name:
        return HttpResponseForbidden("You do not have permission to edit this product.")

    context = {
        'title': 'Edit Product',
        'product': product,
    }

    return render(request, 'fm_goods/edit_product.html', context)


@login
def edit_product_handle(request, goods_id):
    if request.method != 'POST':
        return redirect('fm_goods:index')

    product = get_object_or_404(GoodsInfo, id=goods_id)

    user_name = request.session.get('user_name')
    if product.gunit != user_name:
        return HttpResponseForbidden("You do not have permission to edit this product.")

    gtitle = request.POST.get('gtitle')
    gprice = request.POST.get('gprice')
    gkucun = request.POST.get('gkucun')
    gjianjie = request.POST.get('gjianjie')
    gcontent = request.POST.get('gcontent')

    try:
        product.gtitle = gtitle
        product.gprice = gprice
        product.gkucun = gkucun
        product.gjianjie = gjianjie
        product.gcontent = gcontent

        if 'gpic' in request.FILES:
            product.gpic = request.FILES['gpic']

        product.save()

        messages.success(request, "Product updated successfully.")
        return redirect('fm_goods:detail', goods_id=goods_id)
    except Exception as e:
        messages.error(request, f"Error updating product: {str(e)}")
        return redirect('fm_goods:edit_product', goods_id=goods_id)


@login
def delete_product(request, goods_id):
    product = get_object_or_404(GoodsInfo, id=goods_id)

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
    if request.method != 'POST':
        return redirect('fm_goods:index')

    product = get_object_or_404(GoodsInfo, id=goods_id)

    user_name = request.session.get('user_name')
    if product.gunit != user_name:
        return HttpResponseForbidden("You do not have permission to delete this product.")

    type_id = product.gtype.id

    try:
        product.delete()
        messages.success(request, "Product deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting product: {str(e)}")

    return redirect('fm_goods:list', type_id=type_id, page_index=1, sort=1)