"""
URL configuration for helpdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.models import TicketResource
from . import views

ticket_resource = TicketResource()

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('ticketing/', include(('ticketing.urls', 'ticketing'), namespace='ticketing')),
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),
    path('api/', include(ticket_resource.urls)),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', views.manage_user_groups, name='manage_user_groups'),
]