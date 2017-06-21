from django.conf.urls import url
from utility.views import upload_website, UtilityList

app_name = 'utility_app'
urlpatterns = [
    url(r'^$', UtilityList.as_view(), name='utility_list'),
    url(r'upload_website/$', upload_website, name='utility_upload_website'),
]
