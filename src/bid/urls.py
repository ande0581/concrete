from django.conf.urls import url
from bid import views

app_name = 'bid'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]