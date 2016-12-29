from django.conf.urls import url
from item import views

app_name = 'item'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]