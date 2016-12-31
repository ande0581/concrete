from django.conf.urls import url
from address import views

app_name = 'address_app'
urlpatterns = [
    #url(r'^$', views.customer_model_list_view, name='list'),
    url(r'^create/(?P<customer_id>\d+)/$', views.address_model_create_view, name='create'),
    #url(r'^(?P<pk>\d+)/$', views.customer_model_detail_view, name='detail'),
    #url(r'^(?P<pk>\d+)/delete/$', views.customer_model_delete_view, name='delete'),
    #url(r'^(?P<pk>\d+)/edit/$', views.customer_model_update_view, name='update'),
]