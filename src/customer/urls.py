from django.conf.urls import url
from customer import views

app_name = 'customer_app'
urlpatterns = [
    url(r'^$', views.customer_model_list_view, name='list'),
    url(r'^add/$', views.customer_model_add_view, name='add'),
    url(r'^detail/(?P<pk>\d+)/$', views.customer_model_detail_view, name='detail'),
]