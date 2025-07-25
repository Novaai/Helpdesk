from django.contrib import admin
from .models import Client, Ticket, Helper

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','ticketCategory','severity','date_created','status')

class ClientAdmin(admin.ModelAdmin):
    def client_name(self, obj):
        return str(obj)
    list_display = ['client_name', 'email', 'phone_number', 'department','floor', 'ticket']
    client_name.short_description = "Client name"

class HelperAdmin(admin.ModelAdmin):
    def helper_name(self, obj):
        return str(obj)
    list_display = ['helper_username', 'helper_fname', 'helper_lname', 'email','phone_number']
    helper_name.shortdescription = "Helper name"
# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Helper, HelperAdmin)