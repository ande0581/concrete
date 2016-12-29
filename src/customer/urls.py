from django.conf.urls import url
from customer import views

app_name = 'customer'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_customer/$', views.add_customer, name='add_customer')
]