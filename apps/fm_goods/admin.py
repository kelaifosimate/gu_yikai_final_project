from django.contrib import admin
from .models import TypeInfo, GoodsInfo, GoodsContent


# Register model classes (ordinary method)
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']
    list_per_page = 10
    search_fields = ['ttitle']
    list_display_links = ['ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'gtitle', 'gunit', 'gclick', 'gprice', 'gpic', 'gkucun', 'gjianjie']
    list_editable = ['gkucun', ]
    readonly_fields = ['gclick']
    search_fields = ['gtitle', 'gcontent', 'gjianjie']
    # Fields in the list page that can link to the change_form page
    list_display_links = ['gtitle']


class GoodsContentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'ctitle', 'cpic', 'cusername', 'clogo', 'cuser_content', 'date_publish', 'cgoodsname']
    readonly_fields = ['cuser_content']
    search_fields = ['ctitle', 'cusername', 'cgoodsname']
    list_display_links = ['ctitle']


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(GoodsContent, GoodsContentAdmin)