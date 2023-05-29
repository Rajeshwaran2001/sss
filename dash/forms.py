from django import forms
from .models import Admin
from django.contrib.auth.models import User


class AdminBaseForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['address']

