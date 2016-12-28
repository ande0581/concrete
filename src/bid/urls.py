from django.conf.urls import url
from bid import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]