from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from customer.models import Customer
from customer.forms import CustomerForm


@login_required()
def customer_model_list_view(request):
    queryset_list = Customer.objects.order_by('name')

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(name__icontains=query) |
            Q(telephone__icontains=query) |
            Q(email__icontains=query)
        ).distinct()  # this prevents duplicates

    for customer in queryset_list:
        customer.telephone = "({}) {}-{}".format(customer.telephone[:3], customer.telephone[3:6], customer.telephone[6:])

    paginator = Paginator(queryset_list, 10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {'object_list': queryset}
    return render(request, 'customer/customer_list.html', context)


@login_required()
def customer_model_create_view(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # make modifications here
        form.save()
        messages.success(request, "Customer was created successfully!")
        return redirect('customer_app:detail', pk=obj.pk)
    return render(request, 'customer/customer_create.html', {'form': form})


@login_required()
def customer_model_update_view(request, pk=None):
    obj = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        # make modifications here
        form.save()
        messages.success(request, "Customer was updated successfully!")
        return redirect('customer_app:detail', pk=obj.pk)
    return render(request, 'customer/customer_create.html', {'form': form})


@login_required()
def customer_model_detail_view(request, pk=None):
    obj = get_object_or_404(Customer, pk=pk)
    context = {
        "object": obj,
    }
    return render(request, 'customer/customer_detail.html', context)


@login_required()
def customer_model_delete_view(request, pk=None):
    obj = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Customer was deleted successfully!")
        return redirect('customer_app:list')
    context = {
        "object": obj,
    }
    return render(request, 'customer/customer_delete.html', context)


