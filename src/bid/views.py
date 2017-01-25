from django.db.models import Sum
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from address.models import Address
from bid.models import Bid
from bid_item.models import BidItem
from pdf.models import PDFImage
from bid.forms import BidInitialForm, BidForm


class BidCreate(SuccessMessageMixin, CreateView):
    template_name = 'bid/bid_form.html'
    form_class = BidInitialForm
    success_message = "Successfully Created Bid"

    def get_context_data(self, **kwargs):
        context = super(BidCreate, self).get_context_data(**kwargs)
        #print('VIEW:', context['view'])
        #print('FORM:', context['form'])
        return context

    def form_valid(self, form):
        form.instance.address = Address.objects.get(pk=self.kwargs['address'])
        form.instance.customer = form.instance.address.customer
        #print('FORM_INSTANCE ADDRESS---->', form.instance.address_id)
        #print('FORM_INSTANCE CUSTOMER---->', form.instance.address_id.customer_id)
        #print("POST FORM SAVE:", form.cleaned_data)
        return super(BidCreate, self).form_valid(form)


class BidUpdate(SuccessMessageMixin, UpdateView):

    # TODO Display Photos on bid
    template_name = 'bid/bid_update_form.html'
    model = Bid
    form_class = BidForm
    success_message = "Successfully Updated Bid"

    def get_context_data(self, **kwargs):
        context = super(BidUpdate, self).get_context_data(**kwargs)
        bid_item_obj = BidItem.objects.filter(bid=self.kwargs['pk'])
        context['bid_items'] = bid_item_obj
        context['total_cost'] = bid_item_obj.aggregate(Sum('total'))['total__sum']
        context['pdfs'] = PDFImage.objects.all().filter(bid=self.kwargs['pk'])
        #print('CONTEXT:', context)
        #print('total_cost:', context['total_cost'])
        #print('FORM:', context['form'])
        return context


class BidDelete(DeleteView):
    model = Bid

    def get_object(self, queryset=None):
        # https://ultimatedjango.com/learn-django/lessons/delete-contact-full-lesson/
        # Collect the object before deletion to redirect back to customer detail view on success
        obj = super(BidDelete, self).get_object()
        self.customer_pk = obj.customer.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer_pk})


class BidList(ListView):
    model = Bid

