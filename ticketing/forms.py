from django import forms
from .models import Ticket, Client, FloorChoices, DepartmentChoices, Ticket_category
from django.contrib.auth.models import User, Group

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'  # Load all fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark all fields as readonly except severity, status, and ticket_updates
        editable_fields = ['severity', 'status', 'ticket_updates','ticket_category','tags']


        for field_name, field in self.fields.items():
            if field_name not in editable_fields:
                field.disabled = True  # Makes field read-only

class TicketClientForm(forms.Form):
    title = forms.CharField(label="Ticket Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    ticket_category = forms.ModelChoiceField(
    queryset=Ticket_category.objects.all(),
    widget=forms.Select(attrs={'class': 'form-select'}),
    label="Ticket Category"
)
    ticketDesc = forms.CharField(label="Ticket Description", widget=forms.Textarea(attrs={'class': 'form-control'}))
    
#    class Meta:
#        model = Ticket
#        fields = '__all__'
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        try:
#            group = Group.objects.get(name="Helpdesk Admins")
#            self.fields['assigned_to'].queryset = group.user_set.all()
#        except Group.DoesNotExist:
#            self.fields['assigned_to'].queryset = User.objects.none()



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