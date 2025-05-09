from django.contrib import admin
from .models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["uname", "uemail", "ushou", "uaddress", "uyoubian", "uphone"]
    list_per_page = 5
    search_fields = ["uname", "uemail"]
    readonly_fields = ["uname"]

admin.site.register(UserInfo, UserInfoAdmin)