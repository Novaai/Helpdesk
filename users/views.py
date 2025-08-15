from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.urls import reverse

@never_cache
def login_user(request):
    # Block access if already logged in
    if request.user.is_authenticated:
        if not messages.get_messages(request):  # only add message if none exist
            messages.info(request, "You are already logged in.")
        return redirect('home')

    # Handle login form submission
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error logging in. Please try again.")
            return redirect('custom_login')

    # Show login page
    return render(request, 'authenticate/login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('users:custom_login')

def is_any_admin(user):
    return user.groups.filter(
        name__in=['Helpdesk Admins', 'Inventory Admins', 'General Admins']
    ).exists() or user.is_superuser


@user_passes_test(is_any_admin)
def send_password_reset(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            target_user = User.objects.get(pk=user_id)
            form = PasswordResetForm({'email': target_user.email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='users/password_reset_email.html'
                )
                messages.success(request, f"Password reset link sent to {target_user.email}")
            else:
                messages.error(request, "Invalid email for this user.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
        return redirect('users:send_password_reset')

    users = User.objects.all().order_by('username')
    return render(request, 'users/send_password_reset.html', {'users': users})