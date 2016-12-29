from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect

from customer.models import Customer
from customer.forms import CustomerForm


@login_required()
def index(request):
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

    context_dict = {'object_list': queryset}
    return render(request, 'customer/customer_index.html', context_dict)


@login_required()
def add_customer(request):
    form = CustomerForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        # Have we been provided a valid form?
        if form.is_valid():
            # Save the new customer to the DB
            form.save(commit=True)
            messages.success(request, "Customer was created successfully!")
            return redirect('customer:index')
        else:
            print(form.errors)
    return render(request, 'customer/add_customer.html', {'form': form})

