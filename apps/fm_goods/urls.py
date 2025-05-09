from django.urls import path
from . import views

app_name = 'fm_goods'

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    path('products/', views.ProductList.as_view(), name="list"),
    path('detail/<int:goods_id>/', views.ProductDetail.as_view(), name="detail"),
    path('add_product/', views.add_product, name="add_product"),
    path('add_product_handle/', views.add_product_handle, name="add_product_handle"),
    path('edit_product/<int:goods_id>/', views.edit_product, name="edit_product"),
    path('edit_product_handle/<int:goods_id>/', views.edit_product_handle, name="edit_product_handle"),
    path('delete_product/<int:goods_id>/', views.delete_product, name="delete_product"),
    path('delete_product_handle/<int:goods_id>/', views.delete_product_handle, name="delete_product_handle"),
    path('search/', views.search, name="search"),
]