from django.urls import path
from . import views

app_name = 'fm_cart'

urlpatterns = [
    path('', views.user_cart, name="cart"),
    path('add<int:gid>_<int:count>/', views.add, name="add"),
    path('delete<int:cart_id>/', views.delete, name="delete"),
]