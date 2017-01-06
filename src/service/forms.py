from django import forms
from service.models import Service


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ('description', 'cost', 'category', 'protected')

