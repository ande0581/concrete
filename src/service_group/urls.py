from django.conf.urls import url
from service_group.views import DrivewayCreate


app_name = 'service_group_app'
urlpatterns = [
    url(r'^driveway/(?P<bid>\d+)/$', DrivewayCreate.as_view(), name='driveway_create'),
]