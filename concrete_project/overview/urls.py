from django.conf.urls import url
from overview import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]