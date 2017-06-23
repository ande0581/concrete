from django.conf.urls import url
from .views import ConcreteCreate, StepsCreate, BlockFoundationCreate, \
    PierFootingsCreate, EgressWindowCreate, FloatingSlabCreate, RetainingWallCreate
from .forms import StandardConcreteForm, DecorativeConcreteForm

app_name = 'service_group_app'
urlpatterns = [
    url(r'^standard_concrete/(?P<bid>\d+)/$', ConcreteCreate.as_view(form_class=StandardConcreteForm),
        name='standard_concrete_create'),
    url(r'^decorative_concrete/(?P<bid>\d+)/$', ConcreteCreate.as_view(form_class=DecorativeConcreteForm),
        name='decorative_concrete_create'),
    url(r'^steps/(?P<bid>\d+)/$', StepsCreate.as_view(), name='steps_create'),
    url(r'^foundation/(?P<bid>\d+)/$', BlockFoundationCreate.as_view(), name='foundation_create'),
    url(r'^pier_footings/(?P<bid>\d+)/$', PierFootingsCreate.as_view(), name='pier_footings_create'),
    url(r'^egress_window/(?P<bid>\d+)/$', EgressWindowCreate.as_view(), name='egress_window_create'),
    url(r'^floating_slab/(?P<bid>\d+)/$', FloatingSlabCreate.as_view(), name='floating_slab_create'),
    url(r'^retaining_wall/(?P<bid>\d+)/$', RetainingWallCreate.as_view(), name='retaining_wall_create'),
]
