from django.conf.urls import url
from address import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]