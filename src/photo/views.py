from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView, DeleteView

from bid.models import Bid
from photo.models import Attachment
from photo.forms import UploadForm


class PhotoList(LoginRequiredMixin, ListView):
    model = Attachment
    template_name = 'photo/photo_list.html'

    def get_queryset(self):
        queryset_list = Attachment.objects.filter(bid=self.kwargs['bid_id'])
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data(**kwargs)
        context['bid_id'] = self.kwargs['bid_id']
        return context


class PhotoUpload(LoginRequiredMixin, FormView):

    template_name = 'photo/photo_form.html'
    form_class = UploadForm

    def get_context_data(self, **kwargs):
        context = super(PhotoUpload, self).get_context_data(**kwargs)
        context['bid_id'] = self.kwargs['bid_id']
        return context

    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            bid_obj = Bid.objects.get(pk=self.kwargs['bid_id'])
            Attachment.objects.create(file=each, bid=bid_obj)
        return super(PhotoUpload, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Photo Successfully Uploaded")
        return reverse('photo_app:photo_list', kwargs={'bid_id': self.kwargs['bid_id']})


class PhotoDelete(LoginRequiredMixin, DeleteView):

    model = Attachment
    template_name = 'photo/photo_delete.html'

    def get_object(self, queryset=None):
        obj = super(PhotoDelete, self).get_object()
        self.bid_pk = obj.bid.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('photo_app:photo_list', kwargs={'bid_id': self.bid_pk})
