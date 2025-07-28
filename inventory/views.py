from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def home_inventory(request):
    return render(request, 'home_inventory.html')
