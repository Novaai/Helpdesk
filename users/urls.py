from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name="custom_login"),  # <-- changed to 'login/'
    path('logout/', views.logout_user, name='logout_user'), # <-- consistent naming
    path('admin/send-password-reset/', views.send_password_reset, name='send_password_reset'),
    path('user/password-reset/', views.send_password_reset_non_admin, name='send_password_reset_non_admin'),
    path("register/", views.register_user, name="register"),
    path("role-requests/", views.review_role_requests, name="review_role_requests"),
]
