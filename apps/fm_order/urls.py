from django.urls import path
from . import views

app_name = 'fm_order'

urlpatterns = [
    path('checkout/', views.order_checkout, name="checkout"),
    path('handle/', views.order_handle, name="handle"),
    path('list/', views.OrderList.as_view(), name="list"),
    path('detail/<str:order_id>/', views.OrderDetail.as_view(), name="detail"),
    path('pay/<str:order_id>/', views.pay, name="pay"),
]