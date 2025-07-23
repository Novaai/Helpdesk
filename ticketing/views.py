from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Ticket, Client

# Create your views here.
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
def detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    client = Client.objects.filter(ticket=ticket).first()
    return render(request, 'ticketing/detail.html', {
        'ticket': ticket,
        'client': client,
    })