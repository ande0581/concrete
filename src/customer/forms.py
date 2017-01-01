from django import forms
from customer.models import Customer


class CustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the customer name")
    email = forms.EmailField(max_length=128, help_text="Please enter the customer email address")
    telephone = forms.CharField(min_length=10, max_length=10, help_text="Please enter the customer telephone number")

    class Meta:
        model = Customer
        fields = ('name', 'email', 'telephone')