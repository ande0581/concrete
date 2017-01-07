from django import forms
from address.models import Address

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zip')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Address', css_class='btn=primary'))
