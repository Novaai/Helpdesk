from django.urls import path
from . import views

app_name = 'ticketing'

urlpatterns = [
    path('',views.index, name="index"),
    path('<int:ticket_id>/', views.detail, name='detail'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/client/', views.client_tickets, name='client_tickets'),
    path('tickets/resolved/', views.client_resolved_ticket, name='client_resolved_ticket'),
]