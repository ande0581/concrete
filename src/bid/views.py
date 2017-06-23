from datetime import date
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView


from .models import Bid
from .forms import BidInitialForm, BidForm
from address.models import Address
from bid_item.models import BidItem
from journal.models import Journal
from payment.models import Payment
from pdf.models import PDFImage


def create_bid_item_dict(bid_obj):

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


class BidCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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


class BidDetail(LoginRequiredMixin, SuccessMessageMixin, DetailView):

    template_name = 'bid/bid_detail.html'
    model = Bid

    def get_context_data(self, **kwargs):
        context = super(BidDetail, self).get_context_data(**kwargs)
        bid_obj = Bid.objects.get(id=self.kwargs['pk'])
        bid_item_obj = BidItem.objects.filter(bid=self.kwargs['pk'])
        bid_item_dict = create_bid_item_dict(bid_obj)
        total_cost = bid_item_obj.aggregate(Sum('total'))['total__sum']
        payment_obj = Payment.objects.filter(bid=self.kwargs['pk'])
        total_payments = payment_obj.aggregate(Sum('amount'))['amount__sum']

        context['bid_item_dict'] = bid_item_dict
        context['total_cost'] = total_cost
        context['pdfs'] = PDFImage.objects.all().filter(bid=self.kwargs['pk'])
        context['journal_entries'] = Journal.objects.all().filter(bid=self.kwargs['pk']).order_by('-timestamp')
        context['payments'] = Payment.objects.all().filter(bid=self.kwargs['pk']).order_by('date')
        context['date'] = date.today()

        if total_payments:
            context['remaining_balance'] = total_cost - total_payments
        else:
            context['remaining_balance'] = total_cost

        return context


class BidUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

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


class BidDelete(LoginRequiredMixin, DeleteView):
    model = Bid

    def get_object(self, queryset=None):
        obj = super(BidDelete, self).get_object()
        self.customer_pk = obj.customer.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer_pk})


class BidList(LoginRequiredMixin, ListView):
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

