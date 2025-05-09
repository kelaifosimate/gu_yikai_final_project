from django.urls import path
from . import views

app_name = 'fm_order'

urlpatterns = [
    path('', views.order, name="order"),
    path('push/', views.order_handle, name="push"),
]