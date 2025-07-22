from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket, Client

# Create your views here.
def index(request):
    Tickets_List = Ticket.objects.filter(severity__gte=5)
    #Client.objects.all()
    Clients_List = Client.objects.filter(ticket__isnull=False)
    #output = ', '.join([t.title for t in Tickets_List])
    return render(request,'ticketing/index.html',{'tickets': Tickets_List})
    #output2 = ', '.join([c.first_name for c in Clients_List])
    
    #combined_output = f"Ticket: {output} <br> Client: {output2}"
    #return HttpResponse(combined_output)