from django.conf.urls import url
from customer import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_customer/$', views.add_customer, name='add_customer')
]