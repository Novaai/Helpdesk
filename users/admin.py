from django.contrib import admin
from .models import RoleRequest

@admin.register(RoleRequest)
class RoleRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "requested_group", "status", "created_at", "decided_by", "decided_at")
    list_filter = ("status", "requested_group", "created_at")
    search_fields = ("user__username", "requested_group__name", "note")
