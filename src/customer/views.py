from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Customer
from .forms import CustomerForm
from address.models import Address
from bid.models import Bid
from send_email.models import EmailLog


class CustomerCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'customer/customer_form.html'
    form_class = CustomerForm
    success_message = "Successfully Created: %(first_name)s %(last_name)s"


class CustomerUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    success_message = "Successfully Updated: %(first_name)s %(last_name)s"


class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_list')


class CustomerDetail(LoginRequiredMixin, DetailView):
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(CustomerDetail, self).get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(customer_id=self.kwargs['pk'])
        context['bids'] = Bid.objects.filter(customer_id=self.kwargs['pk'])
        context['emails'] = EmailLog.objects.filter(customer_id=self.kwargs['pk'])
        return context


class CustomerList(LoginRequiredMixin, ListView):
    model = Customer
    paginate_by = 20

    def get_queryset(self):
        queryset_list = Customer.objects.order_by('last_name')
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(company_name__icontains=query) |
                Q(telephone__icontains=query) |
                Q(email__icontains=query)
            ).distinct()

        return queryset_list

