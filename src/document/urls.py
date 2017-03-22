from django.conf.urls import url
from document.views import DocumentList, DocumentCreate, DocumentUpdate, DocumentDelete

app_name = 'document_app'
urlpatterns = [
    url(r'^$', DocumentList.as_view(), name='document_list'),
    url(r'^(?P<pk>\d+)/update/$', DocumentUpdate.as_view(), name='document_update'),
    url(r'^create/$', DocumentCreate.as_view(), name='document_create'),
    url(r'^(?P<pk>\d+)/delete/$', DocumentDelete.as_view(), name='document_delete'),
]