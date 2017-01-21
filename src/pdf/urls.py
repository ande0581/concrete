from django.conf.urls import url
from pdf.views import create_pdf


app_name = 'pdf_app'
urlpatterns = [
    url(r'^create/(?P<bid_id>\d+)/$', create_pdf, name='pdf_create'),
]