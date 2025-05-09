from django.contrib import admin
from .models import OrderInfo, OrderDetailInfo

class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ["oid", "user", "odate", "ototal", "oaddress", "oIsPay"]
    list_per_page = 5
    list_filter = ["oIsPay"]
    search_fields = ["user__uname", "oid"]
    ordering = ["-odate"]

class OrderDetailInfoAdmin(admin.ModelAdmin):
    list_display = ["goods", "order", "price", "count"]
    list_per_page = 5
    search_fields = ["goods__gtitle", "order__oid"]

admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderDetailInfo, OrderDetailInfoAdmin)