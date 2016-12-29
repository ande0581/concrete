from django.conf.urls import url
from accounts import views

app_name = 'customer'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout')
]