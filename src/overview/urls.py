from django.conf.urls import url
from .views import OverviewList


app_name = 'overview_app'
urlpatterns = [
    url(r'^$', OverviewList.as_view(), name='overview_list'),
]