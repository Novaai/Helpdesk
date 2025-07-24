from django import forms
from .models import Ticket, Client, FloorChoices, DepartmentChoices

class TicketClientForm(forms.Form):
    title = forms.CharField(label="Ticket Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticketCategory = forms.CharField(label="Ticket Category", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticketDesc = forms.CharField(label="Ticket Description", widget=forms.Textarea(attrs={'class': 'form-control'}))

    # Client fields
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    floor = forms.ChoiceField(choices=FloorChoices, widget=forms.Select(attrs={'class': 'form-select'}))
    department = forms.ChoiceField(choices=DepartmentChoices, widget=forms.Select(attrs={'class': 'form-select'}))


    # Hidden field for status
    status = forms.ChoiceField(
        choices=Ticket.STATUS_CHOICES,
        initial='pending',
        widget=forms.HiddenInput()
    )