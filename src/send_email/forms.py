from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from document.models import Document

import sys
# http://stackoverflow.com/questions/42024101/problems-with-migrations
# http://stackoverflow.com/questions/39535983/migration-clashes-with-forms-py
if 'makemigrations' in sys.argv or 'migrate' in sys.argv or 'showmigrations' in sys.argv:
    "Prevent querying of DB while initializing the applications, will fail to migrate otherwise"

    def get_queryset():
        pass

else:

    def get_queryset():
        return Document.objects.all()


email_body = """Attached is the proposal for your project. Please let me know if you have any questions.

Thanks,

Tom Madsen - Owner
Madsen Concrete Services
612-508-2484
concrete@madsenservices.com
"""

generic_email_body = """

Tom Madsen - Owner
Madsen Concrete Services
612-508-2484
concrete@madsenservices.com
"""

EMPLOYEES = (('jacobozzzborn@gmail.com', 'Jake Osborn'),
             ('jeffrey.d.anderson@gmail.com', 'Jeff Anderson'),
             ('concrete@madsenservices.com', 'Tom Madsen'),)


class SendCustomerEmailForm(forms.Form):

    body = forms.CharField(initial=email_body, widget=forms.Textarea)
    attachments = forms.ModelMultipleChoiceField(queryset=get_queryset(), required=False,
                                                 label='Select Multiple Attachments by Ctrl-Click')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Send Customer Email', css_class='btn=primary'))


class SendEmployeeEmailForm(forms.Form):
    to_address = forms.EmailField(widget=forms.Select(choices=EMPLOYEES))
    body = forms.CharField(widget=forms.Textarea)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Send Employee Email', css_class='btn=primary'))


class SendGeneralEmailForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(initial=generic_email_body, widget=forms.Textarea)
    attachments = forms.ModelMultipleChoiceField(queryset=get_queryset(), required=False,
                                                 label='Select Multiple Attachments by Ctrl-Click')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Send Customer Email', css_class='btn=primary'))
