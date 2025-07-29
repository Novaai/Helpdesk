from django.urls import path
from . import views

app_name = 'ticketing'

urlpatterns = [
    # Homepage for the ticketing app (e.g., /ticketing/)
    path('', views.home_ticketing, name='home_ticketing'),

    # Detail view for a specific ticket
    path('<int:ticket_id>/', views.detail, name='detail'),

    # Ticket creation form
    path('tickets/create/', views.create_ticket, name='create_ticket'),

    # Client-specific views
    path('tickets/client/', views.client_tickets, name='client_tickets'),
    path('tickets/resolved/', views.client_resolved_ticket, name='client_resolved_ticket'),

    # Replaces the old index view — full ticket list
    path('tickets/all/', views.all_tickets, name='all_tickets'),
]

urlpatterns = [
    # Homepage for the ticketing app
    path('', views.home_ticketing, name='home_ticketing'),
    # Detail view for a specific ticket
    path('<int:ticket_id>/', views.detail, name='detail'),
    # Ticket creation form
    path('ticketing/create/', views.create_ticket, name='create_ticket'),
    # Client-specific views
    path('ticketing/client/', views.client_tickets, name='client_tickets'),
    path('ticketing/resolved/', views.client_resolved_ticket, name='client_resolved_ticket'),
    # View for all tickets
    path('ticketing/all/', views.all_tickets, name='all_tickets'),
]