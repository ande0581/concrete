from django.conf.urls import url
from photo.views import UploadView


app_name = 'photo_app'
urlpatterns = [
    url(r'^upload/(?P<bid_id>\d+)/$', UploadView.as_view(), name='pdf_view'),
]