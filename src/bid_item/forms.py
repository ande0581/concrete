from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import BidItem
from job_type.models import JobType
from service.models import Service


class BidItemForm(forms.ModelForm):
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    description = forms.ModelChoiceField(queryset=Service.objects.all())

    class Meta:
        model = BidItem
        fields = ('job_type', 'description', 'quantity')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Item', css_class='btn=primary'))


class BidItemUpdateForm(forms.ModelForm):

    class Meta:
        model = BidItem
        fields = ('description', 'quantity', 'cost')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Item', css_class='btn=primary'))


class BidItemCustomForm(forms.ModelForm):
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())

    class Meta:
        model = BidItem
        fields = ('job_type', 'description', 'quantity', 'cost')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Custom Item', css_class='btn=primary'))