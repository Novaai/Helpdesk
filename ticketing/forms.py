from django import forms
from .models import Ticket, Client, FloorChoices, DepartmentChoices
from django.contrib.auth.models import User, Group

class TicketClientForm(forms.Form):
    title = forms.CharField(label="Ticket Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticketCategory = forms.CharField(label="Ticket Category", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticketDesc = forms.CharField(label="Ticket Description", widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Ticket
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            group = Group.objects.get(name="Helpdesk Admins")
            self.fields['assigned_to'].queryset = group.user_set.all()
        except Group.DoesNotExist:
            self.fields['assigned_to'].queryset = User.objects.none()

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