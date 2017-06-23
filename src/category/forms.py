from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Category


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'protected']

    def __init__(self, *args, **kwargs):
        """
        If the service.protected value in the db is set to True, change all fields but cost to read-only
        This is done to make sure hardcoded queries don't break if someone modifies the service
        """
        super(CategoryForm, self).__init__(*args, **kwargs)

        if self.initial.get('protected'):
            self.fields['name'].disabled = True
            self.fields['protected'].disabled = True

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Category', css_class='btn=primary'))
