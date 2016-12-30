from django.conf.urls import url
from customer import views

app_name = 'customer_app'
urlpatterns = [
    url(r'^$', views.customer_model_list_view, name='list'),
    url(r'^create/$', views.customer_model_create_view, name='create'),
    url(r'^(?P<pk>\d+)/$', views.customer_model_detail_view, name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.customer_model_update_view, name='update'),
]