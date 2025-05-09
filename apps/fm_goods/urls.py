from django.conf.urls import url, re_path
from django.views.static import serve
from gu_yikai_final_project import settings
from . import views

app_name = 'fm_goods'

urlpatterns = [
    url('^$', views.index, name="index"),
    url('^index/$', views.index, name="index"),
    url('^list(\d+)_(\d+)_(\d+)/$', views.good_list, name="good_list"),
    url('^detail/(\d+)/$', views.detail, name="detail"),
    url('^content/(\d+)/(\d+)/$', views.content, name="content"),
    url(r'^search/', views.ordinary_search, name="ordinary_search"),  # Full-text search
    re_path('^media/(?P<path>.*)/$', serve, {'document_root': settings.MEDIA_ROOT}),
]