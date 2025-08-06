# users/forms.py
from django import forms
from django.contrib.auth.models import User, Group

class BaseUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True, group_name=None):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            if group_name:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
        return user
