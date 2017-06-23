from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Service
from category.models import Category

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
    height = forms.FloatField(label='Height in Inches', required=False)
    width = forms.FloatField(label='Width in Inches', required=False)
    depth = forms.FloatField(label='Depth in Inches', required=False)

    class Meta:
        model = Service
        fields = ('description', 'cost', 'category', 'measurement', 'height', 'width', 'depth', 'protected')

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

    def clean(self):
        """
        If the category is 'Block' or 'Block-Cap' require dimensions get populated in the form
        """
        cleaned_data = super(ServiceForm, self).clean()
        category = cleaned_data.get('category')
        height = cleaned_data.get('height')
        width = cleaned_data.get('width')
        depth = cleaned_data.get('depth')

        if category.name == 'Block' or category.name == 'Block-Cap':
            if height is None or width is None or depth is None:
                raise forms.ValidationError('Category Type is {}. You must enter height, width and depth'.
                                            format(category.name))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Service', css_class='btn=primary'))



