from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from address.models import Address
from bid.models import Bid
from customer.models import Customer
from bid.forms import BidInitialForm, BidForm


class BidCreate(SuccessMessageMixin, CreateView):
    template_name = 'bid/bid_form.html'
    form_class = BidInitialForm
    success_message = "Successfully Created: %(street)s"

    def form_valid(self, form):
        form.instance.customer_id = Customer.objects.get(pk=self.kwargs['customer_id'])
        return super(BidCreate, self).form_valid(form)


class BidUpdate(SuccessMessageMixin, UpdateView):
    model = Bid
    form_class = BidForm
    success_message = "Successfully Updated: %(street)s"


class BidDelete(DeleteView):
    model = Bid

    def get_object(self, queryset=None):
        # https://ultimatedjango.com/learn-django/lessons/delete-contact-full-lesson/
        # Collect the object before deletion to redirect back to customer detail view on success
        obj = super(BidDelete, self).get_object()
        self.customer_pk = Customer.objects.get(id=obj.customer_id)
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_detail', kwargs={'pk': int(self.customer_pk)})


class BidDetail(DetailView):
    model = Bid


class BidList(ListView):
    model = Bid