from django.db.models import Q
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import TicketClientForm
from .models import Ticket, Client
from .forms import TicketUpdateForm
from .utils.reporting import (
    get_status_counts, get_tag_counts,
    generate_pie_chart, generate_bar_chart_from_tags,
    export_status_to_excel, export_tags_to_excel
)

#reporting - charts
def dashboard_view(request):
    timeframe = request.GET.get('timeframe', 'lifetime')

    status_data = get_status_counts(timeframe)
    tags = get_tag_counts(timeframe)

    status_chart = generate_pie_chart(status_data, 'status', 'count')
    tag_chart = generate_bar_chart_from_tags(tags)

    context = {
        'status_chart': status_chart,
        'tag_chart': tag_chart,
        'timeframe': timeframe,
    }
    return render(request, 'ticketing/dashboard.html', context)

#reporting - exports
def export_excel_view(request):
    timeframe = request.GET.get('timeframe', 'lifetime')

    status_data = get_status_counts(timeframe)
    tags = get_tag_counts(timeframe)

    status_excel = export_status_to_excel(status_data)
    tags_excel = export_tags_to_excel(tags)

    # Combine or send as separate files - for simplicity, send status stats:
    response = HttpResponse(
        status_excel.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="ticket_status_stats.xlsx"'
    return response

def is_helpdesk_admin(user):
    return user.groups.filter(name="Helpdesk Admins").exists()

@login_required
@user_passes_test(is_helpdesk_admin)
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticketing:detail', ticket_id=ticket.id)
    else:
        form = TicketUpdateForm(instance=ticket)

    return render(request, 'ticketing/edit_ticket.html', {
        'form': form,
        'ticket': ticket
    })


@login_required
def all_tickets(request):
    query = request.GET.get('q', '')
    tickets = Ticket.objects.all().order_by('-date_created')

    if query:
        tickets = tickets.filter(
            Q(title__icontains=query) |
            Q(client_username__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(severity__icontains=query) |
            Q(status__icontains=query) |
            Q(assigned_to__username__icontains=query)
        ).distinct()

    return render(request, 'ticketing/all_tickets.html', {
        'tickets': tickets,
        'query': query,
    })

@login_required
def detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    client = Client.objects.filter(ticket=ticket).first()
    is_helpdesk_admin = request.user.groups.filter(name="Helpdesk Admins").exists()
    return render(request, 'ticketing/detail.html', {
        'ticket': ticket,
        'client': client,
        'is_helpdesk_admin': is_helpdesk_admin,
    })

@login_required
def client_tickets(request):
    tickets = Ticket.objects.filter(client_username=request.user.username)
    return render(request, 'ticketing/client_ticket.html', {
        'pendingTickets': tickets,
    })

@login_required
def home_ticketing(request):
    return render(request, 'home_ticketing.html')

@login_required
def client_resolved_ticket(request):
    resolved_tickets = Ticket.objects.filter(client_username=request.user.username, status='closed')
    return render(request, 'ticketing/client_resolved_ticket.html', {'resolvedTickets': resolved_tickets})


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketClientForm(request.POST)

        if form.is_valid():
            ticket = Ticket.objects.create(
            title=form.cleaned_data['title'],
            ticket_category=form.cleaned_data['ticket_category'],
            ticketDesc=form.cleaned_data['ticketDesc'],
            status='pending',
            email=request.user.email,
            client_username=request.user.username,
            phone_number=form.cleaned_data['phone_number'],
            )
            Client.objects.create(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
                client_username=request.user.username,
                phone_number=form.cleaned_data['phone_number'],
                floor=form.cleaned_data['floor'],
                department=form.cleaned_data['department'],
                ticket=ticket,
                )
            
            messages.success(request, "Ticket created successfully.")
            #return redirect('ticketing:index')
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TicketClientForm()

    return render(request, 'ticketing/create_ticket.html', {'form': form})
