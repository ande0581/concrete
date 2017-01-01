from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from address.models import Address
from customer.models import Customer
from address.forms import AddressForm


class AddressCreate(SuccessMessageMixin, CreateView):
    template_name = 'address/address_form.html'
    form_class = AddressForm
    success_message = "Successfully Created: %(street)s"

    def form_valid(self, form):
        form.instance.customer_id = Customer.objects.get(pk=self.kwargs['customer_id'])
        return super(AddressCreate, self).form_valid(form)


class AddressUpdate(SuccessMessageMixin, UpdateView):
    model = Address
    form_class = AddressForm
    success_message = "Successfully Updated: %(street)s"


class AddressDelete(DeleteView):
    model = Address

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('address_app:address_list')


class AddressDetail(DetailView):
    model = Address


class AddressList(ListView):
    model = Address


