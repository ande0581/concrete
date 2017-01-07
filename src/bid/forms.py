from django import forms
from bid.models import Bid
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


class BidInitialForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))

    class Meta:
        model = Bid
        fields = ('description', 'scheduled_bid_date', 'notes')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Bid', css_class='btn=primary'))


class BidForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))

    class Meta:
        model = Bid
        fields = ('description', 'notes', 'status', 'scheduled_bid_date',
                  'tentative_start', 'actual_start', 'completion_date', 'down_payment_amount', 'down_payment_date',
                  'final_payment_amount', 'final_payment_date')

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
                Div('down_payment_amount', css_class='col-xs-6'),
                Div('down_payment_date', css_class='col-xs-6'),
                css_class='row-fluid'),
            Div(
                Div('final_payment_amount', css_class='col-xs-6'),
                Div('final_payment_date', css_class='col-xs-6'),
                css_class='row-fluid'),
            FormActions(Submit('Save Bid', 'Save Bid', css_class='btn-primary'))
            )


"""
https://godjango.com/29-crispy-forms/
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


class CreditCardForm(forms.Form):
    fullname = forms.CharField(label="Full Name", required=True)
    card_number = forms.CharField(label="Card", required=True, max_length=16)
    expire = forms.DateField(label="Expire Date", input_formats=['%m/%y'])
    ccv = forms.IntegerField(label="ccv")
    notes = forms.CharField(label="Order Notes", widget=forms.Textarea())

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('fullname', css_class='input-sm'),
        Field('card_number', css_class='input-sm'),
        Field('expire', css_class='input-sm'),
        Field('ccv', css_class='input-sm'),
        Field('notes', rows=3),
        FormActions(Submit('purchase', 'purchase', css_class='btn-primary'))
    )
"""