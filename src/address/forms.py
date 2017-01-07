from django import forms
from address.models import Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zip')
