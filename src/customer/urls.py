# from django.conf.urls import url
# from customer import views

# app_name = 'customer_app'
# urlpatterns = [
#     url(r'^$', views.customer_model_list_view, name='list'),
#     url(r'^create/$', views.customer_model_create_view, name='create'),
#     url(r'^(?P<pk>\d+)/$', views.customer_model_detail_view, name='detail'),
#     url(r'^(?P<pk>\d+)/delete/$', views.customer_model_delete_view, name='delete'),
#     url(r'^(?P<pk>\d+)/edit/$', views.customer_model_update_view, name='update'),
# ]


from django.conf.urls import url
from customer.views import CustomerDetail, CustomerList, CustomerCreate, CustomerUpdate, CustomerDelete


app_name = 'customer_app'
urlpatterns = [
    url(r'^$', CustomerList.as_view(), name='customer_list'),
    url(r'^(?P<pk>\d+)/$', CustomerDetail.as_view(), name='customer_detail'),
    url(r'^(?P<pk>\d+)/update/$', CustomerUpdate.as_view(), name='customer_update'),
    url(r'^create/$', CustomerCreate.as_view(), name='customer_create'),
    url(r'^(?P<pk>\d+)/delete/$', CustomerDelete.as_view(), name='customer_delete'),
]