from django.conf.urls import url
from pdf.views import view_pdf, save_pdf, PDFImageList, PDFImageDelete


app_name = 'pdf_app'
urlpatterns = [
    url(r'^view/(?P<bid_id>\d+)/$', view_pdf, name='pdf_view'),
    url(r'^save/(?P<bid_id>\d+)/$', save_pdf, name='pdf_save'),
    url(r'^list/(?P<pk>\d+)/$', PDFImageList.as_view(), name='pdf_list'),
    url(r'^delete/(?P<pk>\d+)/$', PDFImageDelete.as_view(), name='pdf_delete'),
]