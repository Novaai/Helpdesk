#using tastypie for api. try djangorestframework later for more demanding integrations
from django.db import models
from django.utils import timezone

class Ticket(models.Model):
    title = models.CharField(max_length = 255)
    ticketCategory = models.CharField(max_length = 255)
    severity = models.IntegerField()
    ticketDesc = models.TextField(max_length = 1000)
    date_created = models.DateTimeField(default=timezone.now)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('closed','Closed'),
    ]
    status = models.CharField(max_length = 10,choices=STATUS_CHOICES,default='pending')
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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    floor = models.IntegerField(choices = FloorChoices.choices, default=FloorChoices.NOT_SELECTED)
    department = models.IntegerField(choices = DepartmentChoices.choices, default=DepartmentChoices.NOT_SELECTED)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"