def add_variable_to_context(request):
    context = {}

    if 'user_id' in request.session:
        from apps.fm_user.models import UserInfo
        from apps.fm_cart.models import CartInfo
        from django.contrib.auth.models import User

        user_id = request.session['user_id']

        try:
            user = UserInfo.objects.get(id=user_id)
            cart_count = CartInfo.objects.filter(user_id=user_id).count()

            context['user'] = user
            context['cart_count'] = cart_count
        except UserInfo.DoesNotExist:
            # 尝试获取Django用户
            try:
                django_user = User.objects.get(id=user_id)
                user_info, created = UserInfo.objects.get_or_create(
                    uname=django_user.username,
                    defaults={
                        'upwd': 'django_auth_user',
                        'uemail': django_user.email
                    }
                )
                cart_count = CartInfo.objects.filter(user_id=user_info.id).count()

                context['user'] = user_info
                context['cart_count'] = cart_count
            except User.DoesNotExist:
                pass

    return context