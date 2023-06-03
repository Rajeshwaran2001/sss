from django import forms

from company.models import service


class ServiceBaseForm(forms.ModelForm):
    class Meta:
        model = service
        fields = ['user', 'branch', 'issue', 'pc']


