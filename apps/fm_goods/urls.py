from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'fm_goods'

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),

    # Product detail page
    path('detail/<int:gid>/', views.detail, name="detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)