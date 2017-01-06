from django import forms
from service.models import Service
from category.models import Category


class ServiceForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Service
        fields = ('description', 'cost', 'category')

