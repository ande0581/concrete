from django.conf.urls import url
from journal import views

app_name = 'journal'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]