from django.contrib import admin
from .models import Client, Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','ticketCategory','severity','date_created','status')

class ClientAdmin(admin.ModelAdmin):
    def client_name(self, obj):
        return str(obj)
    list_display = ['client_name', 'email', 'phone_number', 'department','floor', 'ticket']
    client_name.short_description = "Name"

# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(Ticket, TicketAdmin)
