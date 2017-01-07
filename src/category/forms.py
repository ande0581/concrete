from django import forms
from category.models import Category

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name',]

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Category', css_class='btn=primary'))