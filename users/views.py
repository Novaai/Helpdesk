from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.urls import reverse
from .models import RoleRequest
from helpdesk.utils import group_required
from .forms import RegistrationForm
from django.utils import timezone

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


def send_password_reset_non_admin(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email', '').strip()

        # Use the built-in form directly with the email string
        form = PasswordResetForm({'email': user_email})
        if form.is_valid():
            form.save(
                request=request,  # needed to build absolute URLs
                use_https=request.is_secure(),
                email_template_name='users/password_reset_email.html',
                # subject_template_name='users/password_reset_subject.txt',  # optional
                #For live # from_email='no-reply@yourdomain.com',  # optional, else DEFAULT_FROM_EMAIL
            )
            # Always use a neutral message
            messages.success(
                request,
                "If the user is registered, a password reset link has been sent to their email address."
            )
            return redirect('users:custom_login')
        else:
            # Form invalid (bad email format, etc.) – still return neutral wording
            messages.error(
                request,
                "If the user is registered, a password reset link has been sent to their email address."
            )
            return redirect('users:custom_login')

    # GET: render simple form to submit an email address
    return render(request, 'users/submit_reset_email.html')





DEFAULT_ROLE_NAME = "Helpdesk Users"
@never_cache
def register_user(request):
    # If already logged in, keep them out of /register
    if request.user.is_authenticated:
        if not list(messages.get_messages(request)):
            messages.info(request, "You are already logged in.")
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            # Ensure default group exists, then assign
            default_group, _ = Group.objects.get_or_create(name=DEFAULT_ROLE_NAME)
            user.groups.add(default_group)

            # Optional extra role request
            req_group = form.cleaned_data.get("requested_role")
            note = form.cleaned_data.get("note") or ""
            if req_group and not user.groups.filter(id=req_group.id).exists():
                # Avoid duplicate pending requests for same user/group
                exists = RoleRequest.objects.filter(
                    user=user, requested_group=req_group, status="pending"
                ).exists()
                if not exists:
                    RoleRequest.objects.create(
                        user=user,
                        requested_group=req_group,
                        status="pending",
                        note=note,
                    )

            messages.success(request, "Account created. You can now sign in.")
            return redirect('users:custom_login')
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})



@login_required
@group_required("Helpdesk Admins", "Inventory Admins")
def review_role_requests(request):
    pending = RoleRequest.objects.select_related("user", "requested_group").filter(status="pending")

    if request.method == "POST":
        action = request.POST.get("action")
        req_id = request.POST.get("request_id")
        rr = get_object_or_404(RoleRequest, id=req_id, status="pending")

        if action == "approve":
            rr.user.groups.add(rr.requested_group)
            rr.status = "approved"
            rr.decided_at = timezone.now()
            rr.decided_by = request.user
            rr.save()
            messages.success(request, f"Approved {rr.user.username} for role: {rr.requested_group.name}.")
        elif action == "reject":
            rr.status = "rejected"
            rr.decided_at = timezone.now()
            rr.decided_by = request.user
            rr.save()
            messages.info(request, f"Rejected request for {rr.user.username} → {rr.requested_group.name}.")
        return redirect("users:review_role_requests")

    return render(request, "review_role_requests.html", {"pending": pending})
