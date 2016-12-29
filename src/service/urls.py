from django.conf.urls import url
from service import views

app_name = 'service'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]