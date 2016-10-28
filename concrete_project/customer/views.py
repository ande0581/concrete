from django.shortcuts import render
from django.shortcuts import redirect
from customer.models import Customer
from customer.forms import CustomerForm


def index(request):
    customer_list = Customer.objects.order_by('name')
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
            return redirect(index)
        else:
            print(form.errors)
    return render(request, 'customer/add_customer.html', {'form': form})

