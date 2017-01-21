from django.conf.urls import url
from bid.views import BidDetail, BidList, BidCreate, BidUpdate, BidDelete
# from bid.views import PDFView, generate_commercial_invoice


app_name = 'bid_app'
urlpatterns = [
    url(r'^$', BidList.as_view(), name='bid_list'),
    url(r'^(?P<pk>\d+)/$', BidDetail.as_view(), name='bid_detail'),
    #url(r'^(?P<pk>\d+)/pdf/$', PDFView.as_view(), name='bid_pdf'),
    #url(r'^fedex/$', generate_commercial_invoice, name='bid_fedex'),
    url(r'^(?P<pk>\d+)/update/$', BidUpdate.as_view(), name='bid_update'),
    url(r'^create/(?P<address>\d+)/$', BidCreate.as_view(), name='bid_create'),
    url(r'^(?P<pk>\d+)/delete/$', BidDelete.as_view(), name='bid_delete'),
]