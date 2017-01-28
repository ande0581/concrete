from django.contrib import messages
from django.urls import reverse
from django.views.generic import DeleteView
from django.views.generic import ListView

from pdf.pdf_template import generate_pdf
from bid.models import Bid
from pdf.models import PDFImage


def view_pdf(request, **kwargs):

    obj = Bid.objects.get(pk=kwargs['bid_id'])
    response = generate_pdf(request, obj=obj, save_to_disk=False)
    return response


def save_pdf(request, **kwargs):

    obj = Bid.objects.get(pk=kwargs['bid_id'])
    response = generate_pdf(request, obj=obj, save_to_disk=True)
    return response


class PDFImageList(ListView):
    model = PDFImage
    queryset = PDFImage.objects.filter(bid=3)

    def get_context_data(self, **kwargs):
        context = super(PDFImageList, self).get_context_data(**kwargs)
        context['object_list'] = PDFImage.objects.filter(bid=self.kwargs['pk']).order_by('-created_date')
        return context


class PDFImageDelete(DeleteView):
    model = PDFImage

    def get_object(self, queryset=None):
        obj = super(PDFImageDelete, self).get_object()
        self.bid_pk = obj.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('pdf_app:pdf_list', kwargs={'pk': self.bid_pk})




