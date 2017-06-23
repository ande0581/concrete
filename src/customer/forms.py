from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'company_name', 'email', 'telephone')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Customer', css_class='btn=primary'))