from django.contrib import messages
from django.urls import reverse
from django.views.generic import DeleteView
from django.views.generic import ListView

from pdf.pdf_template import generate_pdf
from bid.models import Bid
from bid_item.models import BidItem
from pdf.models import PDFImage


def create_bid_item_dict(bid_obj):
    """
    :param bid_obj:
    :return: dictionary where the key is the job_type and the value is biditem_obj that matches that job_type
    """
    bid_item_obj = BidItem.objects.filter(bid=bid_obj.id)

    unique_job_types = set()
    for item in bid_item_obj:
        unique_job_types.add(item.job_type)

    bid_item_dict = {}
    for job in unique_job_types:
        bid_items = bid_item_obj.filter(job_type=job)
        bid_item_dict.setdefault(job, bid_items)

    return bid_item_dict


def view_pdf(request, **kwargs):

    obj = Bid.objects.get(pk=kwargs['bid_id'])
    bid_item_dict = create_bid_item_dict(obj)
    response = generate_pdf(request, obj=obj, bid_item_dict=bid_item_dict, save_to_disk=False)
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




