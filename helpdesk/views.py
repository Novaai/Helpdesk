from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import group_required


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
@group_required("Helpdesk Admins", "Inventory Admins")
def manage_user_groups(request):
    users = User.objects.all().order_by("username")
    groups = Group.objects.all().order_by("name")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        group_id = request.POST.get("group_id")
        action = request.POST.get("action")

        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)

        if action == "add":
            user.groups.add(group)
        elif action == "remove":
            user.groups.remove(group)

        return redirect("manage_user_groups")

    return render(request, "manage_groups.html", {
        "users": users,
        "groups": groups,
    })