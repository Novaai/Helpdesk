from django.contrib import admin
from .models import Client, Ticket, Helper
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User, Group

class TicketAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title','ticketCategory','severity','date_created','status','ticket_updates')
    readonly_fields = ('assigned_to',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []  # Superusers can edit everything
        elif request.user.is_staff:
            # Make all fields readonly except 'ticket_updates'
            return [field.name for field in self.model._meta.fields if field.name not in ['ticket_updates', 'status']]
        return super().get_readonly_fields(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete

    def has_add_permission(self, request):
        return request.user.is_superuser  # Only superusers can create tickets

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        elif request.user.is_staff:
            return True  # Needed to access form and save changes to allowed fields
        return False
    
class CustomUserAdmin(DefaultUserAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return readonly_fields + ('groups', 'user_permissions', 'is_staff','is_superuser')
        return readonly_fields

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and obj and obj != request.user:
            # Prevent non-superusers from changing other users
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return super().has_add_permission(request)

class CustomGroupAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

# Override default registrations
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)

# Unregister default UserAdmin and re-register with our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class ClientAdmin(admin.ModelAdmin):
    def client_name(self, obj):
        return str(obj)
    list_display = ['id','client_name', 'email', 'phone_number', 'department','floor', 'ticket']
    client_name.short_description = "Client name"

class HelperAdmin(admin.ModelAdmin):
    def helper_name(self, obj):
        return str(obj)
    list_display = ['id','helper_username', 'helper_fname', 'helper_lname', 'email','phone_number']
    helper_name.shortdescription = "Helper name"

# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Helper, HelperAdmin)