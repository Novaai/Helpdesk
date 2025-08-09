from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login_user', views.login_user, name="custom_login"),
    path('logout_user', views.logout_user, name = 'logout_user'),
    path('admin/send-password-reset/', views.send_password_reset, name='send_password_reset'),
]
