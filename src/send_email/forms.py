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
    helper.add_input(Submit('login', 'Send Email', css_class='btn=primary'))
