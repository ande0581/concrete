from django.conf.urls import url
from address.views import AddressList, AddressCreate, AddressUpdate, AddressDelete


app_name = 'address_app'
urlpatterns = [
    url(r'^$', AddressList.as_view(), name='address_list'),
    url(r'^(?P<pk>\d+)/update/$', AddressUpdate.as_view(), name='address_update'),
    url(r'^create/(?P<customer>\d+)/$', AddressCreate.as_view(), name='address_create'),
    url(r'^(?P<pk>\d+)/delete/$', AddressDelete.as_view(), name='address_delete'),
]