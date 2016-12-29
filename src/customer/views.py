from django.contrib import messages
from django.shortcuts import render, redirect
from customer.models import Customer
from customer.forms import CustomerForm


def index(request):
    customer_list = Customer.objects.order_by('name')
    for customer in customer_list:
        customer.telephone = "{}-{}-{}".format(customer.telephone[:3], customer.telephone[3:6], customer.telephone[6:])

    context_dict = {'customers': customer_list}
    return render(request, 'customer/index.html', context_dict)


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
            return redirect(index)
        else:
            print(form.errors)
    return render(request, 'customer/add_customer.html', {'form': form})

