from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView, DeleteView

from .models import Document
from .forms import DocumentForm
from bid.models import Bid


class AttachmentList(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'bid_attachment/bid_attachment_list.html'

    def get_queryset(self):
        queryset_list = Document.objects.filter(bid=self.kwargs['bid_id'])
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(AttachmentList, self).get_context_data(**kwargs)
        context['bid_id'] = self.kwargs['bid_id']
        return context


class AttachmentUpload(LoginRequiredMixin, FormView):

    template_name = 'bid_attachment/bid_attachment_form.html'
    form_class = DocumentForm

    def get_context_data(self, **kwargs):
        context = super(AttachmentUpload, self).get_context_data(**kwargs)
        context['bid_id'] = self.kwargs['bid_id']
        return context

    def form_valid(self, form):
        filename = form.cleaned_data['filename']
        description = form.cleaned_data['description']
        bid_obj = Bid.objects.get(pk=self.kwargs['bid_id'])
        Document.objects.create(filename=filename, description=description, bid=bid_obj)
        return super(AttachmentUpload, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Document Successfully Uploaded")
        return reverse('bid_attachment_app:bid_attachment_list', kwargs={'bid_id': self.kwargs['bid_id']})


class AttachmentDelete(LoginRequiredMixin, DeleteView):

    model = Document
    template_name = 'bid_attachment/bid_attachment_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(AttachmentDelete, self).get_object()
        self.bid_pk = obj.bid.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('bid_attachment_app:bid_attachment_list', kwargs={'bid_id': self.bid_pk})
