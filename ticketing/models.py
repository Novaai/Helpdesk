#using tastypie for api. try djangorestframework later for more demanding integrations
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Ticket_category(models.Model):
    ticket_category_name = models.CharField(max_length=255)
    category_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.ticket_category_name


def get_default_ticket_category():
    return 1

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Ticket(models.Model):
    client_username = models.CharField(max_length = 255, null=True, blank=True)
    title = models.CharField(max_length = 255)
    #ticketCategory = models.CharField(max_length = 255)
    severity = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    ticketDesc = models.TextField(max_length = 1000)
    ticket_updates = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    ticket_category = models.ForeignKey(Ticket_category, on_delete=models.PROTECT, default=get_default_ticket_category)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('closed','Closed'),
    ]
    status = models.CharField(max_length = 10,choices=STATUS_CHOICES,default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    def __str__(self):
        return self.title


class FloorChoices(models.IntegerChoices):
    NOT_SELECTED = 6,'Floor Not Selected'
    GROUND = 0,'Ground Floor'
    ONE = 1,'1st Floor'
    TWO = 2, '2nd Floor'
    THREE = 3,'3rd Floor'
    FOUR = 4, '4th Floor'
    FIVE = 5, '5th Floor'

class DepartmentChoices(models.IntegerChoices):
    NOT_SELECTED = 7,'No Department Selected'
    HRA = 0,'Human Resource Administration'
    PLANNING_AND_INFORMATION = 1,'Planning and Information'
    LGA = 2, 'Local Government Administation'
    RURAL_DEVELOPMENT = 3,'Rural Development'
    EXECUTIVE_OFFICE = 4, 'Office of the Minister'
    PROCUREMENT = 5, 'Procurement Department'
    FINANCE = 6,'Finance Department'

class Client(models.Model):
    client_username = models.CharField(max_length = 255, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    floor = models.IntegerField(choices = FloorChoices.choices, default=FloorChoices.NOT_SELECTED)
    department = models.IntegerField(choices = DepartmentChoices.choices, default=DepartmentChoices.NOT_SELECTED)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"