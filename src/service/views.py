from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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
    # TODO prevent deletion of protected service type
    model = Service

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('service_app:service_list')


class ServiceList(ListView):
    # TODO add search to services list view
    model = Service

    def get_queryset(self, *args, **kwargs):
        qs = super(ServiceList, self).get_queryset(*args, **kwargs).order_by('category')
        return qs



