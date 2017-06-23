from django.conf.urls import url
from .views import ServiceList, ServiceCreate, ServiceUpdate, ServiceDelete

app_name = 'service_app'
urlpatterns = [
    url(r'^$', ServiceList.as_view(), name='service_list'),
    url(r'^(?P<pk>\d+)/update/$', ServiceUpdate.as_view(), name='service_update'),
    url(r'^create/$', ServiceCreate.as_view(), name='service_create'),
    url(r'^(?P<pk>\d+)/delete/$', ServiceDelete.as_view(), name='service_delete'),
]