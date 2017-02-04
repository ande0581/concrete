from django.db.models import Q
from django.db.models import Sum
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from address.models import Address
from bid.models import Bid
from bid_item.models import BidItem
from journal.models import Journal
from pdf.models import PDFImage
from bid.forms import BidInitialForm, BidForm


def create_bid_item_dict(bid_obj):
    """
    :param bid_obj:
    :return: dictionary where the key is the job_type and the value is biditem_obj that matches that job_type
    """
    # items.aggregate(Sum('total'))['total__sum']

    bid_item_obj = BidItem.objects.filter(bid=bid_obj.id)

    unique_job_types = set()
    for item in bid_item_obj:
        unique_job_types.add(item.job_type)

    bid_item_dict = {}
    for job in unique_job_types:
        bid_items = bid_item_obj.filter(job_type=job)
        total = bid_items.aggregate(Sum('total'))['total__sum']
        bid_item_dict.setdefault(job, {})
        bid_item_dict[job]['bid_items'] = bid_items
        bid_item_dict[job]['total'] = total

    return bid_item_dict


class BidCreate(SuccessMessageMixin, CreateView):
    template_name = 'bid/bid_form.html'
    form_class = BidInitialForm
    success_message = "Successfully Created Bid"

    def get_context_data(self, **kwargs):
        context = super(BidCreate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.address = Address.objects.get(pk=self.kwargs['address'])
        form.instance.customer = form.instance.address.customer
        return super(BidCreate, self).form_valid(form)


class BidUpdate(SuccessMessageMixin, UpdateView):

    template_name = 'bid/bid_update_form.html'
    model = Bid
    form_class = BidForm
    success_message = "Successfully Updated Bid"

    def get_context_data(self, **kwargs):
        context = super(BidUpdate, self).get_context_data(**kwargs)
        bid_obj = Bid.objects.get(id=self.kwargs['pk'])
        bid_item_obj = BidItem.objects.filter(bid=self.kwargs['pk'])
        bid_item_dict = create_bid_item_dict(bid_obj)
        context['bid_item_dict'] = bid_item_dict
        context['total_cost'] = bid_item_obj.aggregate(Sum('total'))['total__sum']
        context['pdfs'] = PDFImage.objects.all().filter(bid=self.kwargs['pk'])
        context['journal_entries'] = Journal.objects.all().filter(bid=self.kwargs['pk']).order_by('-timestamp')
        return context


class BidDelete(DeleteView):
    model = Bid

    def get_object(self, queryset=None):
        obj = super(BidDelete, self).get_object()
        self.customer_pk = obj.customer.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer_pk})


class BidList(ListView):
    model = Bid
    paginate_by = 20

    def get_queryset(self):
        queryset_list = Bid.objects.order_by('-timestamp')
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(customer__first_name__icontains=query) |
                Q(customer__last_name__icontains=query) |
                Q(customer__company_name__icontains=query) |
                Q(status__icontains=query)
            ).distinct()

        return queryset_list

