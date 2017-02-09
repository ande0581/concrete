from django.conf.urls import url
from send_email.views import CustomerEmailCreate
from send_email.forms import SendCustomerEmailForm

app_name = 'send_email_app'
urlpatterns = [
    #url(r'^$', CustomerEmailCreate.as_view(), name='customer_email_create'),
    url(r'^create/(?P<pdf_id>\d+)/$', CustomerEmailCreate.as_view(form_class=SendCustomerEmailForm),
        name='customer_email_create'),
]
