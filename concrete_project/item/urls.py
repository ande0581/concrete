from django.conf.urls import url
from item import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]