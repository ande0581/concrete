from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from address.models import Address
from customer.models import Customer
from address.forms import AddressForm


class AddressDetail(DetailView):
    model = Address

    # this is optional
    def get_context_data(self, **kwargs):
        context = super(AddressDetail, self).get_context_data(**kwargs)
        print(context)
        return context


class AddressList(ListView):
    model = Address

    # this is optional
    def get_queryset(self, *args, **kwargs):
        qs = super(AddressList, self).get_queryset(*args, **kwargs).order_by('-street')
        #qs = super(AddressList, self).get_queryset(*args, **kwargs).filter(title__startswith='670')
        print(qs)
        print(qs.first())
        return qs


def index(request):
    return HttpResponse("This is the address page")


@login_required()
def address_model_create_view(request, customer_id=None):
    form = AddressForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # make modifications here
        cust_obj = get_object_or_404(Customer, pk=customer_id)
        obj.customer_id = cust_obj
        form.save()
        messages.success(request, "Address was created successfully!")
        return redirect('customer_app:detail', pk=cust_obj.pk)
    return render(request, 'address/address_create.html', {'form': form})