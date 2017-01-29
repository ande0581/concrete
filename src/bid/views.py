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
        bid_item_obj = BidItem.objects.filter(bid=self.kwargs['pk'])
        context['bid_items'] = bid_item_obj
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

