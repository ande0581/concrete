from django.conf.urls import url
from bid.views import BidList, BidCreate, BidUpdate, BidDelete


app_name = 'bid_app'
urlpatterns = [
    url(r'^$', BidList.as_view(), name='bid_list'),
    url(r'^(?P<pk>\d+)/update/$', BidUpdate.as_view(), name='bid_update'),
    url(r'^create/(?P<address>\d+)/$', BidCreate.as_view(), name='bid_create'),
    url(r'^(?P<pk>\d+)/delete/$', BidDelete.as_view(), name='bid_delete'),
]