from django.conf.urls import url
from .views import PhotoUpload, PhotoList, PhotoDelete


app_name = 'photo_app'
urlpatterns = [
    url(r'^upload/(?P<bid_id>\d+)/$', PhotoUpload.as_view(), name='photo_upload'),
    url(r'^list/(?P<bid_id>\d+)/$', PhotoList.as_view(), name='photo_list'),
    url(r'^delete/(?P<pk>\d+)/$', PhotoDelete.as_view(), name='photo_delete'),
]