from django.conf.urls import url
from .views import JournalCreate, JournalUpdate, JournalDelete


app_name = 'journal_app'
urlpatterns = [
    url(r'^(?P<pk>\d+)/update/$', JournalUpdate.as_view(), name='journal_update'),
    url(r'^create/(?P<bid>\d+)/$', JournalCreate.as_view(), name='journal_create'),
    url(r'^(?P<pk>\d+)/delete/$', JournalDelete.as_view(), name='journal_delete'),
]