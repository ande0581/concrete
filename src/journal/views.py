from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from bid.models import Bid
from journal.models import Journal
from journal.forms import JournalForm


class JournalCreate(SuccessMessageMixin, CreateView):
    template_name = 'address/address_form.html'
    form_class = JournalForm
    success_message = "Successfully Added Journal Entry"

    def form_valid(self, form):
        form.instance.bid = Bid.objects.get(pk=self.kwargs['bid'])
        return super(JournalCreate, self).form_valid(form)


class JournalUpdate(SuccessMessageMixin, UpdateView):
    model = Journal
    form_class = JournalForm
    success_message = "Successfully Updated Journal Entry"


class JournalDelete(DeleteView):
    model = Journal

    def get_object(self, queryset=None):
        # https://ultimatedjango.com/learn-django/lessons/delete-contact-full-lesson/
        # Collect the object before deletion to redirect back to customer detail view on success
        obj = super(JournalDelete, self).get_object()
        self.bid_pk = obj.bid.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('bid_app:bid_update', kwargs={'pk': self.bid_pk})
