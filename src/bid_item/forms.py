from django import forms
from bid_item.models import BidItem

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div


class BidItemForm(forms.ModelForm):

    class Meta:
        model = BidItem
        fields = ('description', 'quantity', 'cost', 'total')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Item', css_class='btn=primary'))