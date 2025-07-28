from django.contrib import admin
from .models import Item, Item_type, Allocation
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User, Group


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id','item_name','item_description','allocation_status']

class Item_typeAdmin(admin.ModelAdmin):
    list_display = ['id','item_type_name', 'item_description']

class AllocationAdmin(admin.ModelAdmin):
    list_display = ['id','staff','item','allocated_on']

# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Item_type, Item_typeAdmin)
admin.site.register(Allocation, AllocationAdmin)