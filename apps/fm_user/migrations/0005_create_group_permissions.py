from __future__ import unicode_literals
from itertools import chain

from django.db import migrations


def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    user_permissions = permission_class.objects.filter(content_type__app_label='fm_user',
                                                       content_type__model='userinfo')

    goods_permissions = permission_class.objects.filter(content_type__app_label='fm_goods',
                                                        content_type__model='goodsinfo')

    cart_permissions = permission_class.objects.filter(content_type__app_label='fm_cart',
                                                       content_type__model='cartinfo')

    order_permissions = permission_class.objects.filter(content_type__app_label='fm_order',
                                                        content_type__model='orderinfo')

    order_detail_permissions = permission_class.objects.filter(content_type__app_label='fm_order',
                                                               content_type__model='orderdetailinfo')

    perm_view_user = permission_class.objects.filter(content_type__app_label='fm_user',
                                                     content_type__model='userinfo',
                                                     codename='view_userinfo')

    perm_view_goods = permission_class.objects.filter(content_type__app_label='fm_goods',
                                                      content_type__model='goodsinfo',
                                                      codename='view_goodsinfo')

    perm_view_cart = permission_class.objects.filter(content_type__app_label='fm_cart',
                                                     content_type__model='cartinfo',
                                                     codename='view_cartinfo')

    perm_view_order = permission_class.objects.filter(content_type__app_label='fm_order',
                                                      content_type__model='orderinfo',
                                                      codename='view_orderinfo')

    perm_view_order_detail = permission_class.objects.filter(content_type__app_label='fm_order',
                                                             content_type__model='orderdetailinfo',
                                                             codename='view_orderdetailinfo')

    regular_user_permissions = chain(
        perm_view_goods,
        perm_view_cart,
        perm_view_order,
        perm_view_order_detail,
        cart_permissions,
        permission_class.objects.filter(content_type__app_label='fm_order', codename='add_orderinfo')  # 可以创建订单
    )

    seller_permissions = chain(
        perm_view_goods,
        perm_view_cart,
        perm_view_order,
        perm_view_order_detail,
        cart_permissions,
        goods_permissions,
        permission_class.objects.filter(content_type__app_label='fm_order', codename='add_orderinfo')
    )

    admin_permissions = chain(
        user_permissions,
        goods_permissions,
        cart_permissions,
        order_permissions,
        order_detail_permissions
    )

    my_groups_initialization_list = [
        {
            "name": "regular_user",
            "permissions_list": regular_user_permissions,
        },
        {
            "name": "seller",
            "permissions_list": seller_permissions,
        },
        {
            "name": "admin",
            "permissions_list": admin_permissions,
        },
    ]
    return my_groups_initialization_list


def add_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            group_object.permissions.set(group['permissions_list'])
            group_object.save()


def remove_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            list_of_permissions = group['permissions_list']
            for permission in list_of_permissions:
                group_object.permissions.remove(permission)
                group_object.save()


class Migration(migrations.Migration):
    dependencies = [
        ('fm_user', '0004_create_groups'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions_data,
            remove_group_permissions_data
        )
    ]