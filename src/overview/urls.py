from django.conf.urls import url
from overview import views

app_name = 'overview'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]