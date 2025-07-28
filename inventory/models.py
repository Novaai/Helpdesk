#using tastypie for api. try djangorestframework later for more demanding integrations
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Item_type(models.Model):
    item_name = models.CharField(max_length = 255)
    item_description = models.EmailField(null=True, blank=True)
    def __str__(self):
        return self.title

class Item(models.Model):
    item_name = models.CharField(max_length = 255)
    #create item type id after creating default choices for item_type
    ALLOCATION_STATUS_CHOICES = [
        ('unallocated', 'Unallocated'),
        ('Allocated','Allocated'),
    ]
    allocation_status = models.CharField(max_length = 10,choices=ALLOCATION_STATUS_CHOICES,default='Unallocated')
    def __str__(self):
        return self.title
    
class Allocation(models.Model):
    staff = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    allocated_on = models.DateField(auto_now_add=True)