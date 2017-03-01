from django import forms
from service.models import Service
from category.models import Category

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

MEASUREMENT_UNITS = [
    ('each', 'each'),
    ('linear_foot', 'linear_foot'),
    ('square_foot', 'square_foot'),
    ('cubic_yard', 'cubic_yard')
]


class ServiceForm(forms.ModelForm):
    # https://www.pydanny.com/overloading-form-fields.html
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    measurement = forms.CharField(widget=forms.Select(choices=MEASUREMENT_UNITS))

    class Meta:
        model = Service
        fields = ('description', 'cost', 'category', 'measurement', 'protected')

    def __init__(self, *args, **kwargs):
        """
        If the service.protected value in the db is set to True, change all fields but cost to read-only
        This is done to make sure hardcoded queries don't break if someone modifies the service
        """
        super(ServiceForm, self).__init__(*args, **kwargs)

        if self.initial.get('protected'):
            self.fields['description'].disabled = True
            self.fields['category'].disabled = True
            self.fields['measurement'].disabled = True
            self.fields['protected'].disabled = True

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Service', css_class='btn=primary'))



