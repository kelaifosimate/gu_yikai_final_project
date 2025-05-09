from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve  # Function for handling uploaded files
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.fm_goods.urls', namespace='fm_goods')),
    path('user/', include('apps.fm_user.urls', namespace='fm_user')),
    path('cart/', include('apps.fm_cart.urls', namespace='fm_cart')),
    path('order/', include('apps.fm_order.urls', namespace='fm_order')),
    path('tinymce/', include('tinymce.urls')),  # Configure URL for rich text editor
]