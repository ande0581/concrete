from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import JobType


class JobTypeForm(forms.ModelForm):

    class Meta:
        model = JobType
        fields = ('description',)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Job Type', css_class='btn=primary'))