from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Item_type(models.Model):
    item_type_name = models.CharField(max_length=255)
    item_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.item_type_name


def get_default_item_type():
    return 1

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_type = models.ForeignKey(Item_type, on_delete=models.PROTECT, default=get_default_item_type)
    ALLOCATION_STATUS_CHOICES = [
        ('unallocated', 'Unallocated'),
        ('allocated', 'Allocated'),
    ]
    allocation_status = models.CharField(
        max_length=11,
        choices=ALLOCATION_STATUS_CHOICES,
        default='unallocated'
    )
    item_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.item_name

class Allocation(models.Model):
    staff = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    allocated_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.item_name} → {self.staff.username}"