from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Journal
from .forms import JournalForm
from bid.models import Bid


class JournalCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'address/address_form.html'
    form_class = JournalForm
    success_message = "Successfully Added Journal Entry"

    def form_valid(self, form):
        form.instance.bid = Bid.objects.get(pk=self.kwargs['bid'])
        return super(JournalCreate, self).form_valid(form)


class JournalUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Journal
    form_class = JournalForm
    success_message = "Successfully Updated Journal Entry"


class JournalDelete(LoginRequiredMixin, DeleteView):
    model = Journal

    def get_object(self, queryset=None):
        obj = super(JournalDelete, self).get_object()
        self.bid_pk = obj.bid.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.bid_pk})
