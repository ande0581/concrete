from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from document.models import Document
from document.forms import DocumentForm


class DocumentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'document/document_form.html'
    form_class = DocumentForm
    success_message = "Successfully Uploaded Document"

    def get_success_url(self):
        return reverse('document_app:document_list')


class DocumentUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    success_message = "Successfully Updated Document"


class DocumentDelete(LoginRequiredMixin, DeleteView):
    model = Document

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted Document")
        return reverse('document_app:document_list')


class DocumentList(LoginRequiredMixin, ListView):
    model = Document

    def get_queryset(self):
        queryset_list = Document.objects.order_by('description')
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(description__icontains=query)
               ).distinct()

        return queryset_list