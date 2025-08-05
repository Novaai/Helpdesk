from django.urls import path
from . import views

app_name = 'ticketing'

#urlpatterns = [
    # Homepage for the ticketing app (e.g., /ticketing/)
#    path('', views.home_ticketing, name='home_ticketing'),

    # Detail view for a specific ticket
#    path('<int:ticket_id>/', views.detail, name='detail'),

    # Ticket creation form
#    path('tickets/create/', views.create_ticket, name='create_ticket'),

    # Client-specific views
#    path('tickets/client/', views.client_tickets, name='client_tickets'),
#    path('tickets/resolved/', views.client_resolved_ticket, name='client_resolved_ticket'),

    # Replaces the old index view — full ticket list
#    path('tickets/all/', views.all_tickets, name='all_tickets'),
#]

urlpatterns = [
    # Homepage for the ticketing app
    path('', views.home_ticketing, name='home_ticketing'),
    # Detail view for a specific ticket
    path('<int:ticket_id>/', views.detail, name='detail'),
    # Edit/Update ticket details as Helpdesk Administrator
    path('<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    # View my assigned tickets (As helpdesk admin)
    path('my-assigned-tickets/', views.my_assigned_tickets, name='my_assigned_tickets'),
    # Ticket creation form
    path('ticketing/create/', views.create_ticket, name='create_ticket'),
    # Client-specific views
    path('ticketing/client/', views.client_tickets, name='client_tickets'),
    path('ticketing/resolved/', views.client_resolved_ticket, name='client_resolved_ticket'),
    # View for all tickets
    path('ticketing/all/', views.all_tickets, name='all_tickets'),
    #views for dashboard (reports) and exports
    path('ticketing/dashboard/', views.dashboard_view, name='dashboard'),
    path('ticketing/export_excel/', views.export_excel_view, name='export_excel'),
]