from django.urls import path
from . import views

app_name = 'fm_user'

urlpatterns = [
    # Authentication
    path('register/', views.register, name="register"),
    path('register_exist/', views.register_exist, name="register_exist"),
    path('login/', views.login_view, name="login"),
    path('login_handle/', views.login_handle, name="login_handle"),
    path('logout/', views.logout, name="logout"),

    # User profile
    path('info/', views.info, name="info"),
    path('order/<int:page>/', views.order, name="order"),
    path('site/', views.site, name="site"),
]