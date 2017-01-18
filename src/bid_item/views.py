from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from bid.models import Bid
from bid_item.models import BidItem
from service.models import Service
from bid_item.forms import BidItemForm, BidItemUpdateForm


class BidItemCreate(SuccessMessageMixin, CreateView):
    template_name = 'bid_item/biditem_form.html'
    form_class = BidItemForm
    success_message = "Successfully Added Item"

    def form_valid(self, form):
        form.instance.bid = Bid.objects.get(pk=self.kwargs['bid'])
        form.instance.cost = Service.objects.values_list('cost').filter(description=form.cleaned_data['description'])[0][0]
        form.instance.total = form.instance.quantity * form.instance.cost
        return super(BidItemCreate, self).form_valid(form)


class BidItemCustomCreate(SuccessMessageMixin, CreateView):
    template_name = 'bid_item/biditem_form.html'
    form_class = BidItemUpdateForm
    success_message = "Successfully Added Item"

    def form_valid(self, form):
        form.instance.bid = Bid.objects.get(pk=self.kwargs['bid'])
        return super(BidItemCustomCreate, self).form_valid(form)


class BidItemUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'bid_item/biditem_form.html'
    model = BidItem
    form_class = BidItemUpdateForm
    success_message = "Successfully Updated Item"


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
