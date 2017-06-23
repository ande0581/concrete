from django.conf.urls import url
from .views import BidList, BidCreate, BidDetail, BidUpdate, BidDelete


app_name = 'bid_app'
urlpatterns = [
    url(r'^$', BidList.as_view(), name='bid_list'),
    url(r'^(?P<pk>\d+)/detail/$', BidDetail.as_view(), name='bid_detail'),
    url(r'^(?P<pk>\d+)/update/$', BidUpdate.as_view(), name='bid_update'),
    url(r'^create/(?P<address>\d+)/$', BidCreate.as_view(), name='bid_create'),
    url(r'^(?P<pk>\d+)/delete/$', BidDelete.as_view(), name='bid_delete'),
]