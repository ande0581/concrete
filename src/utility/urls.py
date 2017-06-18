from django.conf.urls import url
from utility.views import email_website_folder

app_name = 'utility_app'
urlpatterns = [
    url(r'^$', email_website_folder, name='utility_email_website_folder'),
]
