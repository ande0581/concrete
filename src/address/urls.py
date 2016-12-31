from django.conf.urls import url
#from django.views.generic.base import TemplateView

from address.views import address_model_create_view, AddressDetail, AddressList


app_name = 'address_app'
urlpatterns = [
    #url(r'^$', views.customer_model_list_view, name='list'),
    url(r'^$', AddressList.as_view(), name='address_list'),
    url(r'^(?P<pk>\d+)/$', AddressDetail.as_view(), name='address_detail'),
    url(r'^create/(?P<customer_id>\d+)/$', address_model_create_view, name='create'),
    #url(r'^(?P<pk>\d+)/$', views.customer_model_detail_view, name='detail'),
    #url(r'^(?P<pk>\d+)/delete/$', views.customer_model_delete_view, name='delete'),
    #url(r'^(?P<pk>\d+)/edit/$', views.customer_model_update_view, name='update'),
]