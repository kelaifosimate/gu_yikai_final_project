def add_variable_to_context(request):
    """Add common variables to template context"""
    context = {}

    # Add user information if logged in
    if 'user_id' in request.session:
        from apps.fm_user.models import UserInfo
        from apps.fm_cart.models import CartInfo

        try:
            user_id = request.session['user_id']
            user = UserInfo.objects.get(id=user_id)
            cart_count = CartInfo.objects.filter(user_id=user_id).count()

            context['user'] = user
            context['cart_count'] = cart_count
        except UserInfo.DoesNotExist:
            pass

    return context