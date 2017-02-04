from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from bid.models import Bid
from bid_item.models import BidItem
from service.models import Service
from bid_item.forms import BidItemForm, BidItemCustomForm, BidItemUpdateForm


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
    form_class = BidItemCustomForm
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
        obj = super(BidItemDelete, self).get_object()
        self.bid_pk = obj.bid.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('bid_app:bid_update', kwargs={'pk': self.bid_pk})


class BidItemGroupDelete(DeleteView):
    # http://stackoverflow.com/questions/16606762/using-two-parameters-to-delete-using-a-django-deleteview

    model = BidItem

    def get_object(self, queryset=None):

        # Job name spaces were replaced with dunders when generating url, reversing that modification
        job_name = self.kwargs['job_name'].replace('__', ' ')

        context = job_name
        return context

    def delete(self, request, *args, **kwargs):
        bid_id = self.kwargs['bid_id']

        # Job name spaces were replaced with dunders when generating url, reversing that modification
        job_name = self.kwargs['job_name'].replace('__', ' ')

        biditemgroup = BidItem.objects.filter(bid_id=bid_id, job_type=job_name)
        biditemgroup.delete()

        messages.success(self.request, "Successfully Deleted Job")
        return HttpResponseRedirect(reverse('bid_app:bid_update', kwargs={'pk': bid_id}))

