from django import forms
from payment.models import Payment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ('date', 'description', 'amount')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Payment', css_class='btn=primary'))