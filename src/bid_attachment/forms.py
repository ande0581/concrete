from django import forms
from bid_attachment.models import Document

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('description', 'filename')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Upload Document', css_class='btn=primary'))
