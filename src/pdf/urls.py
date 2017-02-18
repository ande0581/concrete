from django.conf.urls import url
from pdf.views import view_pdf, save_pdf, PDFImageList, PDFImageDelete


app_name = 'pdf_app'
urlpatterns = [
    url(r'^view/(?P<bid_id>\d+)/proposal/$', view_pdf, name='pdf_view_proposal_customer'),
    url(r'^view/(?P<bid_id>\d+)/invoice/$', view_pdf, {'invoice': True}, name='pdf_view_invoice'),
    url(r'^save/(?P<bid_id>\d+)/proposal/$', save_pdf, name='pdf_save_proposal'),
    url(r'^save/(?P<bid_id>\d+)/invoice/$', save_pdf, {'invoice': True}, name='pdf_save_invoice'),
    url(r'^list/(?P<pk>\d+)/$', PDFImageList.as_view(), name='pdf_list'),
    url(r'^delete/(?P<pk>\d+)/$', PDFImageDelete.as_view(), name='pdf_delete'),
]