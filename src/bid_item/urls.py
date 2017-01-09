from django.conf.urls import url
from bid_item.views import BidItemCreate, BidItemUpdate, BidItemDelete


app_name = 'bid_item_app'
urlpatterns = [
    # url(r'^$', BidList.as_view(), name='bid_list'),
    # url(r'^(?P<pk>\d+)/$', BidDetail.as_view(), name='bid_detail'),
    # url(r'^(?P<pk>\d+)/pdf/$', PDFView.as_view(), name='bid_pdf'),
    url(r'^(?P<pk>\d+)/update/$', BidItemUpdate.as_view(), name='bid_item_update'),
    url(r'^create/(?P<bid>\d+)/$', BidItemCreate.as_view(), name='bid_item_create'),
    url(r'^(?P<pk>\d+)/delete/$', BidItemDelete.as_view(), name='bid_item_delete'),
]