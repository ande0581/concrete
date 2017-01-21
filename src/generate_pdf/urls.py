from django.conf.urls import url
from generate_pdf.views import create_pdf


app_name = 'generate_pdf_app'
urlpatterns = [
    url(r'^$', create_pdf, name='generate_pdf_app_create'),
    # url(r'^(?P<pk>\d+)/$', CustomerDetail.as_view(), name='customer_detail'),
    # url(r'^(?P<pk>\d+)/update/$', CustomerUpdate.as_view(), name='customer_update'),
    # url(r'^create/$', CustomerCreate.as_view(), name='customer_create'),
    # url(r'^(?P<pk>\d+)/delete/$', CustomerDelete.as_view(), name='customer_delete'),
]