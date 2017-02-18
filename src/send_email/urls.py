from django.conf.urls import url
from send_email.views import CustomerEmailCreate, EmployeeEmailCreate
from send_email.forms import SendCustomerEmailForm, SendEmployeeEmailForm

app_name = 'send_email_app'
urlpatterns = [
    #url(r'^$', CustomerEmailCreate.as_view(), name='customer_email_create'),
    url(r'^customer_create/(?P<pdf_id>\d+)/$', CustomerEmailCreate.as_view(form_class=SendCustomerEmailForm),
        name='customer_email_create'),
    url(r'^employee_create/(?P<bid_id>\d+)/$', EmployeeEmailCreate.as_view(form_class=SendEmployeeEmailForm),
        name='employee_email_create'),
]
