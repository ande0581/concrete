from django.conf.urls import url
from bid_attachment.views import AttachmentUpload, AttachmentList, AttachmentDelete


app_name = 'bid_attachment_app'
urlpatterns = [
    url(r'^upload/(?P<bid_id>\d+)/$', AttachmentUpload.as_view(), name='bid_attachment_upload'),
    url(r'^list/(?P<bid_id>\d+)/$', AttachmentList.as_view(), name='bid_attachment_list'),
    url(r'^delete/(?P<pk>\d+)/$', AttachmentDelete.as_view(), name='bid_attachment_delete'),
]