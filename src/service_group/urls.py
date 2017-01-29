from django.conf.urls import url
from service_group.views import StandardConcreteCreate, DecorativeConcreteCreate, StepsCreate, FoundationCreate, \
    FootingsCreate, EgressWindowCreate

app_name = 'service_group_app'
urlpatterns = [
    url(r'^standard_concrete/(?P<bid>\d+)/$', StandardConcreteCreate.as_view(), name='standard_concrete_create'),
    url(r'^decorative_concrete/(?P<bid>\d+)/$', DecorativeConcreteCreate.as_view(), name='decorative_concrete_create'),
    url(r'^steps/(?P<bid>\d+)/$', StepsCreate.as_view(), name='steps_create'),
    url(r'^foundation/(?P<bid>\d+)/$', FoundationCreate.as_view(), name='foundation_create'),
    url(r'^footings/(?P<bid>\d+)/$', FootingsCreate.as_view(), name='footings_create'),
    url(r'^egress_window/(?P<bid>\d+)/$', EgressWindowCreate.as_view(), name='egress_window_create')
]
