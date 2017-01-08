from django import forms
from service.models import Service

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div


class DrivewayForm(forms.Form):
    length = forms.IntegerField(label='Length in Feet', required=False)
    width = forms.IntegerField(label='Width in Feet', required=False)
    thickness = forms.IntegerField(label='Thickness in Inches', required=False)
    cement_type = forms.ModelChoiceField(queryset=Service.objects.all().filter(category__name__exact='Cement'))
    rebar_type = forms.ModelChoiceField(queryset=Service.objects.all().filter(category__name__exact='Rebar'))
    fill = forms.ModelChoiceField(queryset=Service.objects.all().filter(category__name__exact='Fill'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Driveway', css_class='btn=primary'))