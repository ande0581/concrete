from django.conf.urls import url
from .views import CategoryList, CategoryCreate, CategoryUpdate, CategoryDelete

app_name = 'category_app'
urlpatterns = [
    url(r'^$', CategoryList.as_view(), name='category_list'),
    url(r'^(?P<pk>\d+)/update/$', CategoryUpdate.as_view(), name='category_update'),
    url(r'^create/$', CategoryCreate.as_view(), name='category_create'),
    url(r'^(?P<pk>\d+)/delete/$', CategoryDelete.as_view(), name='category_delete'),
]