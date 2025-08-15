# users/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

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


#Registration Form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    requested_role = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False,
        empty_label="(No extra role)"
    )
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Reason for requesting this role (optional)"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "requested_role", "note")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style (Bootstrap-friendly names if you want)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
        # Hide the default role from requests; they'll get it automatically anyway
        self.fields["requested_role"].queryset = Group.objects.exclude(name="Helpdesk Users").order_by("name")
