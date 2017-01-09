from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from address.models import Address
from bid.models import Bid
from bid_item.models import BidItem
from bid_item.forms import BidItemForm


class BidItemCreate(SuccessMessageMixin, CreateView):
    template_name = 'bid_item/biditem_form.html'
    form_class = BidItemForm
    success_message = "Successfully Added Item"

    # def get_context_data(self, **kwargs):
    #     context = super(BidItemCreate, self).get_context_data(**kwargs)
    #     #print('VIEW:', context['view'])
    #     #print('FORM:', context['form'])
    #     return context

    def form_valid(self, form):
        form.instance.bid = Bid.objects.get(pk=self.kwargs['bid'])
        return super(BidItemCreate, self).form_valid(form)


class BidItemUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'bid_item/biditem_form.html'
    model = BidItem
    form_class = BidItemForm
    success_message = "Successfully Updated Item"

    # def get_context_data(self, **kwargs):
    #     context = super(BidItemUpdate, self).get_context_data(**kwargs)
    #     context['bid_items'] = BidItem.objects.filter(bid=self.kwargs['pk'])
    #     print('CONTEXT:', context)
    #     print('BID:', context['bid'].address.street)
    #     #print('FORM:', context['form'])
    #     return context


class BidItemDelete(DeleteView):
    model = BidItem

    def get_object(self, queryset=None):
        # https://ultimatedjango.com/learn-django/lessons/delete-contact-full-lesson/
        # Collect the object before deletion to redirect back to customer detail view on success
        obj = super(BidItemDelete, self).get_object()
        self.bid_pk = obj.bid.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('bid_app:bid_update', kwargs={'pk': self.bid_pk})
