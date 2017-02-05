from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from bid.models import Bid
from payment.models import Payment
from payment.forms import PaymentForm


class PaymentCreate(SuccessMessageMixin, CreateView):
    template_name = 'payment/payment_form.html'
    form_class = PaymentForm
    success_message = "Successfully Added Payment"

    def form_valid(self, form):
        form.instance.bid = Bid.objects.get(pk=self.kwargs['bid_id'])
        return super(PaymentCreate, self).form_valid(form)


class PaymentUpdate(SuccessMessageMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    success_message = "Successfully Updated Payment"


class PaymentDelete(DeleteView):
    model = Payment

    def get_object(self, queryset=None):
        obj = super(PaymentDelete, self).get_object()
        self.bid_pk = obj.bid.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted Payment")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.bid_pk})
