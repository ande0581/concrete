"""concrete_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from overview import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^address/', include('address.urls')),
    url(r'^bid/', include('bid.urls')),
    url(r'^calculator/', include('calculator.urls')),
    url(r'^customer/', include('customer.urls')),
    url(r'^item/', include('item.urls')),
    url(r'^journal/', include('journal.urls')),
    url(r'^overview/', include('overview.urls')),
    url(r'^service/', include('service.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
