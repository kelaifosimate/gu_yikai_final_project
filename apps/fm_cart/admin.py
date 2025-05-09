from django.contrib import admin
from .models import CartInfo

class CartInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'count']
    list_per_page = 5
    search_fields = ['user__uname', 'goods__gtitle']

admin.site.register(CartInfo, CartInfoAdmin)