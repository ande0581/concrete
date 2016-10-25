from django.conf.urls import url
from journal import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]