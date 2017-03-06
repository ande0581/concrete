from django import forms
from bid.models import Bid

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div


class BidInitialForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}), required=False)

    class Meta:
        model = Bid
        fields = ('description', 'scheduled_bid_date', 'notes')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Bid', css_class='btn=primary'))


class BidForm(forms.ModelForm):
    # https://godjango.com/29-crispy-forms/
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}), required=False)

    class Meta:
        model = Bid
        fields = ('description', 'notes', 'status', 'scheduled_bid_date',
                  'tentative_start', 'actual_start', 'completion_date', 'custom_down_payment',
                  'billto_name', 'billto_street', 'billto_city_st_zip', 'billto_telephone')

    helper = FormHelper()
    helper.layout = Layout(
            Div(
                Div('description', css_class='col-xs-12'),
                css_class='row-fluid'),
            Div(
                Div('notes', css_class='col-xs-12'),
                css_class='row-fluid'),
            Div(
                Div('status', css_class='col-xs-12'),
                css_class='row-fluid'),
            Div(
                Div('scheduled_bid_date', css_class='col-xs-6'),
                Div('tentative_start', css_class='col-xs-6'),
                css_class='row-fluid'),
            Div(
                Div('actual_start', css_class='col-xs-6'),
                Div('completion_date', css_class='col-xs-6'),
                css_class='row-fluid'),
            Div(
                Div('custom_down_payment', css_class='col-xs-12'),
                css_class='row-fluid'),
            Div(
                Div('billto_name', css_class='col-xs-12'),
                css_class='row-fluid'),
            Div(
                Div('billto_street', css_class='col-xs-12'),
                css_class='row-fluid'),
            Div(
                Div('billto_city_st_zip', css_class='col-xs-12'),
                css_class='row-fluid'),
            Div(
                Div('billto_telephone', css_class='col-xs-12'),
                css_class='row-fluid'),
            FormActions(Submit('Save Bid', 'Save Bid', css_class='btn-primary'))
            )
