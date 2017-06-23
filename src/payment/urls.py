from django.conf.urls import url
from .views import PaymentCreate, PaymentUpdate, PaymentDelete


app_name = 'payment_app'
urlpatterns = [
    url(r'^(?P<bid_id>\d+)/create/$', PaymentCreate.as_view(), name='payment_create'),
    url(r'^(?P<pk>\d+)/update/$', PaymentUpdate.as_view(), name='payment_update'),
    url(r'^(?P<pk>\d+)/delete/$', PaymentDelete.as_view(), name='payment_delete'),
]