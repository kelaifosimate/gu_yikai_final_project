from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from . import views

app_name = 'fm_goods'

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    re_path(r'^list(\d+)_(\d+)_(\d+)/$', views.good_list, name="good_list"),
    re_path(r'^detail/(\d+)/$', views.detail, name="detail"),
    re_path(r'^content/(\d+)/(\d+)/$', views.content, name="content"),
    path('search/', views.ordinary_search, name="ordinary_search"),  # Full-text search
    re_path(r'^media/(?P<path>.*)/$', serve, {'document_root': settings.MEDIA_ROOT}),
]