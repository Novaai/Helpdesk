from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="custom_login"),
    path('logout_user', views.logout_user, name = 'logout_user'),
]