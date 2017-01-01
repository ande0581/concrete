from django.core.urlresolvers import reverse

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from address.models import Address
from customer.models import Customer
from address.forms import AddressForm


# class ExampleCreate(CreateView):
#     model = Example
#     fields = ['street', 'state', 'city', 'zip', 'customer_id']
#
#     # optional template, or it defaults to example_form.html
#     template_name = "xxx.html"
#
#     # optional form, when you use this, you omit the fields = []
#     form_class = ExampleForm
#
#     # to change a value after the form is posted
#     def form_valid(self, form):
#         #print('form.instance:', form.instance)
#         #print('kwargs:', self.kwargs)
#         form.instance.customer_id = Customer.objects.get(pk=self.kwargs['customer_id'])
#         #print('form.instance.customer_id:', form.instance.customer_id)
#         return super(ExampleCreate, self).form_valid(form)


# class ExampleUpdate(UpdateView):
#     model = Example
#
#     # you use fields or form_class but not both
#     #fields = ['street', 'city', 'state', 'zip']
#
#     form_class = ExampleForm
#
#     # template name is option
#     template_name = 'form.html'


# class ExampleDelete(DeleteView):
#     model = Example
#
#     def get_success_url(self):
#         return reverse('address_app:address_list')


# class ExampleDetail(DetailView):
#     model = Example
#
#     # this is optional to see the context
#     def get_context_data(self, **kwargs):
#         context = super(ExampleDetail, self).get_context_data(**kwargs)
#         print(context)
#         return context


# class ExampleList(ListView):
#     model = Example
#
#     # this is optional way to change the queryset
#     def get_queryset(self, *args, **kwargs):
#         qs = super(ExampleList, self).get_queryset(*args, **kwargs).order_by('-street')
#         #qs = super(ExampleList, self).get_queryset(*args, **kwargs).filter(title__startswith='670')
#         print(qs)
#         print(qs.first())
#         return qs