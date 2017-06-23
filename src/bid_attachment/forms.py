from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Document


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('description', 'filename')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Upload Document', css_class='btn=primary'))
