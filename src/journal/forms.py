from django import forms
from journal.models import Journal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class JournalForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))

    class Meta:
        model = Journal
        fields = ('body',)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Journal Entry', css_class='btn=primary'))