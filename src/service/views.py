from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from service.models import Service
from service.forms import ServiceForm


class ServiceCreate(SuccessMessageMixin, CreateView):
    template_name = 'service/service_form.html'
    form_class = ServiceForm
    success_message = "Successfully Created Service"

    def get_success_url(self):
        return reverse('service_app:service_list')


class ServiceUpdate(SuccessMessageMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    success_message = "Successfully Updated Service"


class ServiceDelete(DeleteView):
    model = Service

    def get_object(self, queryset=None):
        # Do not allow the deletion of a protected service which is hardcoded in queries
        obj = super(ServiceDelete, self).get_object()
        if obj.protected:
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('service_app:service_list')


class ServiceList(ListView):
    # TODO add search to services list view
    model = Service

    def get_queryset(self, *args, **kwargs):
        qs = super(ServiceList, self).get_queryset(*args, **kwargs).order_by('category')
        return qs



