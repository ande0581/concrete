from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import FormView
from photo.forms import UploadForm
from photo.models import Attachment


class UploadView(FormView):

    # TODO Name files on upload
    template_name = 'photo/photo_form.html'
    form_class = UploadForm

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        print(self.kwargs)
        context['bid_id'] = self.kwargs['bid_id']
        return context

    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            Attachment.objects.create(file=each)
        return super(UploadView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Photos Successfully Uploaded")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid_id']})