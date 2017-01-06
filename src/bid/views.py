from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

from address.models import Address
from bid.models import Bid
from customer.models import Customer
from bid.forms import BidInitialForm, BidForm, DrivewayForm


class BidCreate(SuccessMessageMixin, CreateView):
    template_name = 'bid/bid_form.html'
    form_class = BidInitialForm
    success_message = "Successfully Created Bid"

    def get_context_data(self, **kwargs):
        context = super(BidCreate, self).get_context_data(**kwargs)
        #print('VIEW:', context['view'])
        #print('FORM:', context['form'])
        return context

    def form_valid(self, form):
        form.instance.address_id = Address.objects.get(pk=self.kwargs['address_id'])
        form.instance.customer_id = form.instance.address_id.customer_id
        #print('FORM_INSTANCE ADDRESS---->', form.instance.address_id)
        #print('FORM_INSTANCE CUSTOMER---->', form.instance.address_id.customer_id)
        #print("POST FORM SAVE:", form.cleaned_data)
        return super(BidCreate, self).form_valid(form)


class DrivewayCreate(SuccessMessageMixin, FormView):
    template_name = 'bid/bid_form.html'
    form_class = DrivewayForm
    #success_message = "Successfully Created Bid"

    def get_success_url(self):
        #messages.success(self.request, "Successfully Deleted")
        return reverse('bid_app:driveway_create')

    def get_context_data(self, **kwargs):
        context = super(DrivewayCreate, self).get_context_data(**kwargs)
        # print('VIEW:', context['view'])
        # print('FORM:', context['form'])
        return context

    def form_valid(self, form):
        #print('%%%%%%%', form.__dict__)
        #print("POST FORM SAVE:", form.cleaned_data)
        cement_cost, cement_type = form.cleaned_data['cement_type'].split('|')
        #print('CEMENT COST:', cement_cost)
        #print('CEMENT TYPE:', cement_type)
        return super(DrivewayCreate, self).form_valid(form)


class BidUpdate(SuccessMessageMixin, UpdateView):
    model = Bid
    form_class = BidForm
    success_message = "Successfully Updated Bid"


class BidDelete(DeleteView):
    model = Bid

    def get_object(self, queryset=None):
        # https://ultimatedjango.com/learn-django/lessons/delete-contact-full-lesson/
        # Collect the object before deletion to redirect back to customer detail view on success
        obj = super(BidDelete, self).get_object()
        self.customer_pk = obj.customer_id.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer_pk})


class BidDetail(DetailView):
    model = Bid


class BidList(ListView):
    model = Bid