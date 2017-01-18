from django import forms
from bid_item.models import BidItem
from service.models import Service

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div


class BidItemForm(forms.ModelForm):
    description = forms.ModelChoiceField(queryset=Service.objects.all().order_by('description'))

    class Meta:
        model = BidItem
        fields = ('description', 'quantity')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Item', css_class='btn=primary'))


class BidItemUpdateForm(forms.ModelForm):
    # TODO, post save calculate quantity x cost

    class Meta:
        model = BidItem
        fields = ('description', 'quantity')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Item', css_class='btn=primary'))


class BidItemCustomForm(forms.ModelForm):
        class Meta:
            model = BidItem
            fields = ('description', 'total')

        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('login', 'Save Custom Item', css_class='btn=primary'))