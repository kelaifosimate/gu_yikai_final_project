from django.contrib import admin

from .models import OrderDetailInfo, OrderInfo
from apps.fm_user.models import ReturnInfo


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    # Fields to display in the list page, by default all fields will be shown
    list_display = ["oid", "user", "odate", "ototal", "oaddress"]
    # Number of entries to display per page
    list_per_page = 5
    # Filters on the right side, must be fields, can inherit from SimpleListFilter to customize filter fields and rules
    list_filter = ["user", "odate", "oaddress"]
    # Fields that can be fuzzy searched on the list page
    search_fields = ["user__uname"]
    ordering = ["-odate"]


@admin.register(OrderDetailInfo)
class OrderDetailInfoAdmin(admin.ModelAdmin):
    list_display = ["goods", "order", "price", "count"]
    list_per_page = 5
    list_filter = ["goods"]

@admin.register(ReturnInfo)
class ReturnInfoAdmin(admin.ModelAdmin):
    # Fields to display in the list page, by default all fields will be shown
    list_display = ["title", "username", "username1", "person_number", "order_number", "kuaidi", "kuaidi_number", "address", "address1", "text", "passOrdefault", "date_publish"]
    # Number of entries to display per page
    list_per_page = 5
    # Filters on the right side, must be fields, can inherit from SimpleListFilter to customize filter fields and rules
    list_filter = ["title", "username", "username1", "order_number"]
    # Fields that can be fuzzy searched on the list page
    search_fields = ["username"]
    ordering = ["-order_number"]