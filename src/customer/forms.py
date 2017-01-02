from django import forms
from customer.models import Customer

# alternative to crispy forms
# {{ form.as_p }}


class CustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter the customer name")
    email = forms.EmailField(max_length=128, required=False, help_text="Enter the customer email address")
    telephone = forms.CharField(min_length=10, max_length=10, required=False,
                                help_text="Enter the customer telephone number")

    class Meta:
        model = Customer
        fields = ('name', 'email', 'telephone')