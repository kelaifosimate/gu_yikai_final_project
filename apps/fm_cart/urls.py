from django.urls import path
from . import views

app_name = 'fm_cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add<int:goods_id>_<int:count>/', views.add, name='add'),
    path('update<int:cart_id>_<int:count>/', views.update, name='update'),
    path('delete<int:cart_id>/', views.delete, name='delete'),
]