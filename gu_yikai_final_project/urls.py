from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # About page for non-logged in users
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    # App URLs
    path('', include('apps.fm_goods.urls')),
    path('user/', include('apps.fm_user.urls')),
    path('cart/', include('apps.fm_cart.urls')),
    path('order/', include('apps.fm_order.urls')),

    # Authentication
    path('login/', LoginView.as_view(template_name='fm_user/login.html'), name='login_urlpattern'),
    path('logout/', LogoutView.as_view(), name='logout_urlpattern'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)