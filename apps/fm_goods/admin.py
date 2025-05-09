from django.contrib import admin
from .models import GoodsInfo

class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'gtitle', 'gunit', 'gclick', 'gprice', 'gkucun', 'gjianjie']
    list_editable = ['gkucun']
    readonly_fields = ['gclick']
    search_fields = ['gtitle', 'gjianjie']
    list_display_links = ['gtitle']

admin.site.register(GoodsInfo, GoodsInfoAdmin)