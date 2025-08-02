from django import forms
from .models import Item, Item_type, Allocation
from django.contrib.auth.models import User, Group

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_type', 'item_description']  # Add other editable fields here if needed

        widgets = {
            'item_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
        }

class AddItemForm(forms.Form):
    item_name = forms.CharField(
        label="Item Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    item_type = forms.ModelChoiceField(
        queryset=Item_type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Item Type"
    )

    item_description = forms.CharField(
        label="Item Description",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    allocation_status = forms.ChoiceField(
        label="Item Allocation Status",
        choices=[('unallocated', 'Unallocated'), ('allocated', 'Allocated')],
        initial='unallocated',
        widget=forms.HiddenInput()
    )

    allocated_to = forms.ChoiceField(
        label="Allocate to:",
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['allocated_to'].choices = [('', 'Unallocated')] + [
            (user.pk, user.username) for user in User.objects.order_by('username')
        ]