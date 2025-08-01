from django import forms
from .models import Item
from django.contrib.auth.models import User

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_type', 'item_description']  # Add other editable fields here if needed

        widgets = {
            'item_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
        }