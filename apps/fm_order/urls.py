from django.conf.urls import url

from . import views

app_name = 'fm_order'

urlpatterns = [
    url(r'^$', views.order, name="order"),
    url(r'^push/$', views.order_handle, name="push"),
]