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

    def clean(self):
        """
        If the category is 'Block' or 'Block-Cap' require dimensions get populated in the form
        """
        cleaned_data = super(JobTypeForm, self).clean()
        description = cleaned_data.get('description')

        if '.' in description:
            raise forms.ValidationError('You cannot use a period (.) in the description')