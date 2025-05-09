from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.urls import reverse
from apps.fm_user import user_decorator
from apps.fm_user.models import UserInfo, Information
from .models import GoodsInfo, TypeInfo, GoodsContent, ContentChart
from apps.fm_cart.models import CartInfo
from apps.fm_order.models import OrderDetailInfo
from apps.fm_user.models import GoodsBrowser
from datetime import datetime
from django.contrib import messages


def index(request):
    # Query the latest 4 and hottest 4 items for each category
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    # Contact customer service
    # Display messages
    username1 = "customer"
    informations = Information.objects.filter()
    # Check if user has sent a message to customer service
    informations1 = Information.objects.filter(cusername1=username, cusername=username1)
    import datetime
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current time
    # Message reply
    user_name = UserInfo.objects.get(uname=username1)  # Get current message user info
    # Display reply messages
    if request.method == "POST":
        cusername = user.uname
        cusername1 = user_name.uname
        ccontent_chart = request.POST.get('title')
        cinformation_id = user_name.id
        if ccontent_chart == "":
            messages.success(request, "Please enter content!")
        else:
            Information.objects.create(cusername=cusername, cusername1=cusername1,
                                       ccontent_chart=ccontent_chart, cinformation_id=cinformation_id)
            messages.success(request, "Message sent successfully")
            return redirect(reverse("fm_goods:index"))
    typelist = TypeInfo.objects.all()
    #  _set table join operation
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]  # By upload order
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]  # By click count
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    cart_num = 0
    # Check if there is a login status
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': 'Home',
        'cart_num': cart_num,
        'guest_cart': 1,
        'type0': type0, 'type01': type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type51,
        'user': user,
        'informations': informations,
        'informations1': informations1,
        'username1': username1,
        'user_name': user_name,
        'nowTime': nowTime,
    }

    return render(request, 'fm_goods/index.html', context)


def good_list(request, tid, pindex, sort):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    # tid: product category information, pindex: product page number, sort: product display sorting method
    typeinfo = TypeInfo.objects.get(pk=int(tid))

    # Find the current product category by primary key
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # Latest product recommendations on the left side of list.html
    goods_list = []
    # Product display method in the middle column of list
    cart_num, guest_cart = 0, 0

    try:
        user_id = request.session['user_id']
    except:
        user_id = None
    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    if sort == '1':  # Default latest
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':  # By price
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':  # By popularity (click count)
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    # Create a Paginator object
    paginator = Paginator(goods_list, 4)
    # Return a Page object containing product information
    page = paginator.page(int(pindex))
    context = {
        'title': 'Product List',
        'guest_cart': guest_cart,
        'cart_num': cart_num,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,  # Sorting method
        'news': news,
        'user': user,
    }
    return render(request, 'fm_goods/list.html', context)


def detail(request, gid):
    if 'user_id' in request.session:
        uid = request.session['user_id']
        user = UserInfo.objects.get(id=uid)
        good_id = gid
        goods = GoodsInfo.objects.get(pk=int(good_id))
        goods.gclick = goods.gclick + 1  # Product click count
        goods.save()

        news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {
            'title': goods.gtype.ttitle,
            'guest_cart': 1,
            'cart_num': cart_count(request),
            'goods': goods,
            'news': news,
            'id': good_id,
            'user': user,
        }
        response = render(request, 'fm_goods/detail.html', context)

        try:
            browsed_good = GoodsBrowser.objects.get(user_id=int(uid), good_id=int(good_id))
        except Exception:
            browsed_good = None
        if browsed_good:
            from datetime import datetime
            browsed_good.browser_time = datetime.now()
            browsed_good.save()
        else:
            GoodsBrowser.objects.create(user_id=int(uid), good_id=int(good_id))
            browsed_goods = GoodsBrowser.objects.filter(user_id=int(uid))
            browsed_good_count = browsed_goods.count()
            if browsed_good_count > 5:
                ordered_goods = browsed_goods.order_by("-browser_time")
                for _ in ordered_goods[5:]:
                    _.delete()
        return response

    else:
        good_id = gid
        goods = GoodsInfo.objects.get(pk=int(good_id))
        news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {
            'title': goods.gtype.ttitle,
            'guest_cart': 0,
            'cart_num': cart_count(request),
            'goods': goods,
            'news': news,
            'id': good_id,
        }
        return render(request, 'fm_goods/detail.html', context)


# Comment
def content(request, gid, pindex):
    if 'user_id' in request.session:
        uid = request.session['user_id']
        user = UserInfo.objects.get(id=uid)
        good_id = gid
        goods = GoodsInfo.objects.get(pk=int(good_id))
        # Get current product information
        news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        # Conditional query
        goodsContents = GoodsContent.objects.filter(cgoodsname_id=good_id).order_by('-date_publish')

        print("Current product comment count:")
        print(goodsContents.count())
        # Order information
        goodsOrderDetailInfos = OrderDetailInfo.objects.filter()
        # Create a Paginator object
        paginator = Paginator(goodsContents, 2)
        # Return a Page object containing product information
        page = paginator.page(int(pindex))
        for goodsContent in page:
            if goodsContent.cgoodsname_id == goods.id:
                content_id = goodsContent.id

        context = {
            'title': goods.gtype.ttitle,
            'guest_cart': 1,
            'cart_num': cart_count(request),
            'goods': goods,
            'id': good_id,
            'news': news,
            'user': user,
            'goodsContents': goodsContents,
            'paginator': paginator,
            'page': page,
            'goodsOrderDetailInfos': goodsOrderDetailInfos,
        }
        if request.method == "POST":
            ctitle = goods.gtitle
            cpic = request.FILES.get('pic')
            cusername = user.uname
            clogo = user.ulogo
            cuser_content = request.POST.get('text')
            cgoodsname_id = goods.id
            if cpic == "":
                GoodsContent.objects.create(ctitle=ctitle, cusername=cusername, cuser_content=cuser_content, cgoodsname_id=cgoodsname_id, clogo=clogo)
                messages.success(request, "Comment successful!")
            else:
                GoodsContent.objects.create(ctitle=ctitle, cpic=cpic, cusername=cusername, cuser_content=cuser_content, cgoodsname_id=cgoodsname_id, clogo=clogo)
                messages.success(request, "Comment successful!")

        return render(request, 'fm_goods/content.html', context)
    else:
        good_id = gid
        goods = GoodsInfo.objects.get(pk=int(good_id))
        # Get current product information
        news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        # Conditional query
        goodsContents = GoodsContent.objects.filter(cgoodsname_id=good_id).order_by('-date_publish')

        print("Current product comment count:")
        print(goodsContents.count())
        # Order information
        goodsOrderDetailInfos = OrderDetailInfo.objects.filter()
        # Create a Paginator object
        paginator = Paginator(goodsContents, 2)
        # Return a Page object containing product information
        page = paginator.page(int(pindex))
        for goodsContent in page:
            if goodsContent.cgoodsname_id == goods.id:
                content_id = goodsContent.id

        context = {
            'title': goods.gtype.ttitle,
            'guest_cart': 0,
            'cart_num': cart_count(request),
            'goods': goods,
            'id': good_id,
            'news': news,
            'goodsContents': goodsContents,
            'paginator': paginator,
            'page': page,
            'goodsOrderDetailInfos': goodsOrderDetailInfos,
        }
        return render(request, 'fm_goods/content.html', context)


@user_decorator.login
def cart_count(request):
    if 'user_id' in request.session:
        return CartInfo.objects.filter(user_id=request.session['user_id']).count
    else:
        return 0


def ordinary_search(request):
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    from django.db.models import Q

    search_keywords = request.GET.get('q', '')
    pindex = request.GET.get('pindex', 1)
    search_status = 1
    cart_num, guest_cart = 0, 0

    try:
        user_id = request.session['user_id']
    except:
        user_id = None

    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    goods_list = GoodsInfo.objects.filter(
        Q(gtitle__icontains=search_keywords) |
        Q(gcontent__icontains=search_keywords) |
        Q(gjianjie__icontains=search_keywords)).order_by("gclick")

    if goods_list.count() == 0:
        # Product search result is empty, return recommended products
        search_status = 0
        goods_list = GoodsInfo.objects.all().order_by("gclick")[:4]

    paginator = Paginator(goods_list, 4)
    page = paginator.page(int(pindex))

    context = {
        'title': 'Search Results',
        'search_status': search_status,
        'guest_cart': guest_cart,
        'cart_num': cart_num,
        'page': page,
        'paginator': paginator,
        'user': user,
    }
    return render(request, 'fm_goods/ordinary_search.html', context)