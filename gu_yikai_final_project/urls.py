from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.fm_goods.urls')),
    path('user/', include('apps.fm_user.urls')),

    # Only include the minimum necessary URLs for basic functionality
    path('cart/', include('apps.fm_cart.urls')),
    path('order/', include('apps.fm_order.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)