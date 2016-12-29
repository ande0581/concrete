from django.conf.urls import url
from address import views

app_name = 'address'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]