from django.conf.urls import url
from job_type.views import JobTypeList, JobTypeCreate, JobTypeUpdate, JobTypeDelete

app_name = 'job_type_app'
urlpatterns = [
    url(r'^$', JobTypeList.as_view(), name='job_type_list'),
    url(r'^(?P<pk>\d+)/update/$', JobTypeUpdate.as_view(), name='job_type_update'),
    url(r'^create/$', JobTypeCreate.as_view(), name='job_type_create'),
    url(r'^(?P<pk>\d+)/delete/$', JobTypeDelete.as_view(), name='job_type_delete'),
]