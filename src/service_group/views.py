from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

from service.models import Service
from service_group.forms import DrivewayForm


def calculate_sq_ft(length, width, inches):
    return length * width * (inches / 12)


class DrivewayCreate(SuccessMessageMixin, FormView):
    """
    (length x width x thickness) / 27 = yards

    """
    template_name = 'service_group/driveway_form.html'
    form_class = DrivewayForm

    def get_success_url(self):
        messages.success(self.request, "Driveway Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    def get_context_data(self, **kwargs):
        context = super(DrivewayCreate, self).get_context_data(**kwargs)
        #print('VIEW:', context['view'])
        #print('FORM:', context['form'])
        return context

    def form_valid(self, form):
        #print('%%%%%%%', form.__dict__)
        print("POST FORM SAVE:", form.cleaned_data)
        length = form.cleaned_data['length']
        width = form.cleaned_data['width']
        thickness = form.cleaned_data['thickness']
        concrete = form.cleaned_data['concrete_type']
        rebar = form.cleaned_data['rebar_type']
        fill = form.cleaned_data['fill']

        sq_ft = calculate_sq_ft(length, width, thickness)
        print('sq_ft:', sq_ft)
        print('cement:', concrete)
        print('rebar:', rebar)
        if fill:
            print('fill:', fill)
        #cement_cost, cement_type = form.cleaned_data['cement_type'].split('|')
        #print('CEMENT COST:', cement_cost)
        #print('CEMENT TYPE:', cement_type)
        return super(DrivewayCreate, self).form_valid(form)
