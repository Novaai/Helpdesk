from django.db import models
from tastypie.resources import ModelResource
from ticketing.models import Ticket

class TicketResource(ModelResource):
    class Meta:
        queryset = Ticket.objects.all()
        resource_name = 'ticketing'
        excludes = [] #any exclusions e.g 'date_created'