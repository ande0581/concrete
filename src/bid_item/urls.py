from django.conf.urls import url
from .views import BidItemCreate, BidItemCustomCreate, BidItemUpdate, BidItemDelete, BidItemGroupDelete


app_name = 'bid_item_app'
urlpatterns = [
    url(r'^create/(?P<bid>\d+)/$', BidItemCreate.as_view(), name='bid_item_create'),
    url(r'^create_custom/(?P<bid>\d+)/$', BidItemCustomCreate.as_view(), name='bid_item_custom_create'),
    url(r'^(?P<pk>\d+)/update/$', BidItemUpdate.as_view(), name='bid_item_update'),
    url(r'^(?P<pk>\d+)/delete/$', BidItemDelete.as_view(), name='bid_item_delete'),
    url(r'^(?P<bid_id>\d+)/(?P<job_name>\w+)/group_delete/$', BidItemGroupDelete.as_view(),
        name='bid_item_group_delete'),
]