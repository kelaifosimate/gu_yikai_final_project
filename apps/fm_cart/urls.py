from django.urls import path, re_path
from . import views

app_name = 'fm_cart'

urlpatterns = [
    path('', views.user_cart, name="cart"),
    re_path(r'^add(\d+)_(\d+)/$', views.add, name="add"),
    re_path(r'^edit(\d+)_(\d+)/$', views.edit, name="edit"),
    re_path(r'^delete(\d+)/$', views.delete, name="delete"),
]