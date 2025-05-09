from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from . import views

app_name = 'fm_user'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('register_handle/', views.register_handle, name="register_handle"),
    path('register_exist/', views.register_exist, name="register_exist"),
    path('login/', views.login, name="login"),
    path('login_handle/', views.login_handle, name="login_handle"),
    path('info/', views.info, name="info"),
    re_path(r'^order/(\d+)$', views.order, name="order"),
    path('site/', views.site, name="site"),
    path('publishers/', views.publishers, name="publishers"),
    path('changeInformation/', views.changeInformation, name="changeInformation"),
    path('check_user/', views.check_user, name="check_user"),
    path('myself_information/', views.myself_information, name="myself_information"),
    re_path(r'^seller_information/(.+)/$', views.seller_information, name="seller_information"),
    path('message/', views.message, name="message"),
    path('person_message/', views.person_message, name="person_message"),
    path('logout/', views.logout, name="logout"),
    path('changeInPwd/', views.changeInPwd, name="changeInPwd"),
    path('findpwdView/', views.findpwdView, name="findpwdView"),
    path('return_item/', views.return_item, name="return_item"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]