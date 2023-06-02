from django import forms
from .models import Admin
from django.contrib.auth.models import User
from utility.models import device_list
from django.forms.widgets import DateInput


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


class asset_listForm(forms.ModelForm):
    class Meta:
        model = device_list
        fields = ['branch', 'user', 'sys_name', 'warranty', 'system_purchased_from', 'bill_no', 'system_purchased_year',
                  'manufacture', 'processor', 'ram', 'hard_disk_type', 'hard_disk_size', 'monitor', 'ip_address',
                  'printer', 'printer_purchased_from', 'printer_year']
        widgets = {
            'system_purchased_year': DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'printer_year': DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
        }


class asset_editForm(forms.ModelForm):
    class Meta:
        model = device_list
        fields = ['branch', 'user', 'sys_name', 'warranty', 'barcode_id', 'system_purchased_from', 'bill_no',
                  'system_purchased_year',
                  'manufacture', 'processor', 'ram', 'hard_disk_type', 'hard_disk_size', 'monitor', 'ip_address',
                  'printer', 'printer_purchased_from', 'printer_year']
        widgets = {
            'system_purchased_year': DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'printer_year': DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
        }
