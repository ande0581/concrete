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

    def get_context_data(self, **kwargs):
        context = super(ServiceUpdate, self).get_context_data(**kwargs)
        #print('VIEW:', context['view'])
        #print('FORM:', context['form'])
        return context

    def form_valid(self, form):
        #print('%%%%%%%', self.__dict__)
        print("POST FORM SAVE:", form.cleaned_data)
        #cement_cost, cement_type = form.cleaned_data['cement_type'].split('|')
        #print('CEMENT COST:', cement_cost)
        #print('CEMENT TYPE:', cement_type)
        return super(ServiceUpdate, self).form_valid(form)


class ServiceDelete(DeleteView):
    model = Service

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('service_app:service_list')


class ServiceList(ListView):
    model = Service
    # TODO sort by category

    def get_queryset(self, *args, **kwargs):
        qs = super(ServiceList, self).get_queryset(*args, **kwargs).order_by('category')
        return qs



