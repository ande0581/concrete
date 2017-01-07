from django.conf.urls import url
from bid.views import BidDetail, BidList, BidCreate, BidUpdate, BidDelete, DrivewayCreate


app_name = 'bid_app'
urlpatterns = [
    url(r'^$', BidList.as_view(), name='bid_list'),
    url(r'^(?P<pk>\d+)/$', BidDetail.as_view(), name='bid_detail'),
    url(r'^(?P<pk>\d+)/update/$', BidUpdate.as_view(), name='bid_update'),
    url(r'^create/(?P<address>\d+)/$', BidCreate.as_view(), name='bid_create'),
    url(r'^(?P<pk>\d+)/delete/$', BidDelete.as_view(), name='bid_delete'),
    url(r'^driveway/$', DrivewayCreate.as_view(), name='driveway_create'),
]