from django.conf.urls import url
from send_email.views import ProposalInvoiceEmailCreate, EmployeeEmailCreate, GeneralEmailCreate
from send_email.forms import SendCustomerEmailForm, SendEmployeeEmailForm, SendGeneralEmailForm

app_name = 'send_email_app'
urlpatterns = [
    url(r'^customer_create/(?P<pdf_id>\d+)/$', ProposalInvoiceEmailCreate.as_view(form_class=SendCustomerEmailForm),
        name='customer_email_create'),
    url(r'^employee_create/(?P<bid_id>\d+)/$', EmployeeEmailCreate.as_view(form_class=SendEmployeeEmailForm),
        name='employee_email_create'),
    url(r'^general_create/(?P<customer_id>\d+)/$', GeneralEmailCreate.as_view(form_class=SendGeneralEmailForm),
        name='general_email_create'),
]
