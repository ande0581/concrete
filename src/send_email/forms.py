from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div


email_body = """Attached is the proposal for your project. Please let me know if you have any questions.

Thanks,

Tom
"""


class SendCustomerEmailForm(forms.Form):

    body = forms.CharField(initial=email_body, widget=forms.Textarea)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Send Customer Email', css_class='btn=primary'))


class SendEmployeeEmailForm(forms.Form):
    to_address = forms.EmailField(initial='jeffrey.d.anderson@gmail.com')
    body = forms.CharField(widget=forms.Textarea)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Send Employee Email', css_class='btn=primary'))
