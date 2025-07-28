from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TicketClientForm
from .models import Ticket, Client
@login_required
def index(request):
    pendingTickets = Ticket.objects.filter(status='pending')
    #Client.objects.all()
    clients = Client.objects.filter(ticket__isnull=False)
    #output = ', '.join([t.title for t in Tickets_List])
    #return render(request,'ticketing/index.html',{'tickets': Tickets_List})
    return render(request,'ticketing/index.html',{'clients': clients,
                                                  'pendingTickets':pendingTickets})
    #output2 = ', '.join([c.first_name for c in Clients_List])
    
    #combined_output = f"Ticket: {output} <br> Client: {output2}"
    #return HttpResponse(combined_output)
@login_required
def detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    client = Client.objects.filter(ticket=ticket).first()
    return render(request, 'ticketing/detail.html', {
        'ticket': ticket,
        'client': client,
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
            ticketCategory=form.cleaned_data['ticketCategory'],
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
