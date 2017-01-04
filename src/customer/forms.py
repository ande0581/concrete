from django import forms
from customer.models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'company_name', 'email', 'telephone')