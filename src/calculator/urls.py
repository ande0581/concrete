from django.conf.urls import url
from calculator import views

app_name = 'calculator'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]