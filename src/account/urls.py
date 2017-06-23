from django.conf.urls import url
from .views import login_view, logout_view

app_name = 'account_app'
urlpatterns = [
    url(r'^login/$', login_view, name='login_view'),
    url(r'^logout/$', logout_view, name='logout_view')
]