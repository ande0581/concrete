from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from address.models import Address
from customer.models import Customer
from address.forms import AddressForm


class AddressCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'address/address_form.html'
    form_class = AddressForm
    success_message = "Successfully Created: %(street)s"

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(pk=self.kwargs['customer'])
        return super(AddressCreate, self).form_valid(form)


class AddressUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Address
    form_class = AddressForm
    success_message = "Successfully Updated: %(street)s"


class AddressDelete(LoginRequiredMixin, DeleteView):
    model = Address

    def get_object(self, queryset=None):
        obj = super(AddressDelete, self).get_object()
        self.customer_pk = obj.customer.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer_pk})



