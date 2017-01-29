from django import forms
from bid_item.models import BidItem
from job_type.models import JobType
from service.models import Service

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div


class BidItemForm(forms.ModelForm):
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    description = forms.ModelChoiceField(queryset=Service.objects.all().order_by('description'))

    class Meta:
        model = BidItem
        fields = ('job_type', 'description', 'quantity')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Item', css_class='btn=primary'))


class BidItemUpdateForm(forms.ModelForm):
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    # TODO, way to keep default job_type value on update?

    class Meta:
        model = BidItem
        fields = ('job_type', 'description', 'quantity', 'cost')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Item', css_class='btn=primary'))


class BidItemCustomForm(forms.ModelForm):
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())

    class Meta:
        model = BidItem
        fields = ('job_type', 'description', 'total')

        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('login', 'Save Custom Item', css_class='btn=primary'))