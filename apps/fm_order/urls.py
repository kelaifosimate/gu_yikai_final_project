from django.urls import path
from . import views

app_name = 'fm_order'

urlpatterns = [
    path('', views.order, name="order"),
    path('handle/', views.order_handle, name="handle"),
    path('list/<int:page>/', views.order_list, name="list"),
    path('detail/<str:order_id>/', views.order_detail, name="detail"),
]