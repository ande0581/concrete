from django import forms
from address.models import Address


class AddressForm(forms.ModelForm):
    street = forms.CharField(max_length=128, help_text="Please enter the street address")
    city = forms.CharField(max_length=128, help_text="Please enter the city")
    state = forms.CharField(max_length=2, help_text="Please enter the 2 digit state abbreviation")
    zip = forms.CharField(max_length=5, help_text="Please enter the 5 digit zipcode")

    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zip')