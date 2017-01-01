from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.db.models import Q

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from customer.models import Customer
from customer.forms import CustomerForm


class CustomerCreate(SuccessMessageMixin, CreateView):
    template_name = 'customer/customer_form.html'
    form_class = CustomerForm
    success_message = "Successfully Created: %(name)s"


class CustomerUpdate(SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    success_message = "Successfully Updated: %(name)s"


class CustomerDelete(DeleteView):
    model = Customer

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_list')


class CustomerDetail(DetailView):
    model = Customer


class CustomerList(ListView):
    model = Customer
    # TODO change pagination value to something larger
    paginate_by = 5

    def get_queryset(self):
        queryset_list = Customer.objects.order_by('name')
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query) |
                Q(telephone__icontains=query) |
                Q(email__icontains=query)
            ).distinct()  # this prevents duplicates

        for customer in queryset_list:
            if len(customer.telephone) == 10:
                customer.telephone = "({}) {}-{}".format(customer.telephone[:3], customer.telephone[3:6],
                                                     customer.telephone[6:])

        return queryset_list

