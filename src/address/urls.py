from django.conf.urls import url
from address.views import AddressDetail, AddressList, AddressCreate


app_name = 'address_app'
urlpatterns = [
    url(r'^$', AddressList.as_view(), name='address_list'),
    url(r'^(?P<pk>\d+)/$', AddressDetail.as_view(), name='address_detail'),
    url(r'^create/(?P<customer_id>\d+)/$', AddressCreate.as_view(), name='address_create'),
]