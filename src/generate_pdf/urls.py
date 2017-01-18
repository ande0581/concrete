from django.conf.urls import url
from generate_pdf.views import print_users


app_name = 'generate_pdf_app'
urlpatterns = [
    url(r'^$', print_users, name='customer_list'),
    # url(r'^(?P<pk>\d+)/$', CustomerDetail.as_view(), name='customer_detail'),
    # url(r'^(?P<pk>\d+)/update/$', CustomerUpdate.as_view(), name='customer_update'),
    # url(r'^create/$', CustomerCreate.as_view(), name='customer_create'),
    # url(r'^(?P<pk>\d+)/delete/$', CustomerDelete.as_view(), name='customer_delete'),
]