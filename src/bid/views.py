from django.db.models import Sum
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.template import RequestContext
import os

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from wkhtmltopdf.views import PDFTemplateView

from address.models import Address
from bid.models import Bid
from bid_item.models import BidItem
from bid.forms import BidInitialForm, BidForm


class PDFView(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'bid/bid_pdf.html'

    def get_context_data(self, **kwargs):
        context = super(PDFView, self).get_context_data(**kwargs)
        print("PDF Context:", context)
        obj = Bid.objects.get(pk=context['pk'])
        context = {'obj': obj}
        print('Post PDF Context:', context)
        return context


class BidCreate(SuccessMessageMixin, CreateView):
    template_name = 'bid/bid_form.html'
    form_class = BidInitialForm
    success_message = "Successfully Created Bid"

    def get_context_data(self, **kwargs):
        context = super(BidCreate, self).get_context_data(**kwargs)
        #print('VIEW:', context['view'])
        #print('FORM:', context['form'])
        return context

    def form_valid(self, form):
        form.instance.address = Address.objects.get(pk=self.kwargs['address'])
        form.instance.customer = form.instance.address.customer
        #print('FORM_INSTANCE ADDRESS---->', form.instance.address_id)
        #print('FORM_INSTANCE CUSTOMER---->', form.instance.address_id.customer_id)
        #print("POST FORM SAVE:", form.cleaned_data)
        return super(BidCreate, self).form_valid(form)


class BidUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'bid/bid_update_form.html'
    model = Bid
    form_class = BidForm
    success_message = "Successfully Updated Bid"

    def get_context_data(self, **kwargs):
        context = super(BidUpdate, self).get_context_data(**kwargs)
        bid_item_obj = BidItem.objects.filter(bid=self.kwargs['pk'])
        context['bid_items'] = bid_item_obj
        context['total_cost'] = bid_item_obj.aggregate(Sum('total'))['total__sum']
        #print('CONTEXT:', context)
        #print('total_cost:', context['total_cost'])
        #print('FORM:', context['form'])
        return context


class BidDelete(DeleteView):
    model = Bid

    def get_object(self, queryset=None):
        # https://ultimatedjango.com/learn-django/lessons/delete-contact-full-lesson/
        # Collect the object before deletion to redirect back to customer detail view on success
        obj = super(BidDelete, self).get_object()
        self.customer_pk = obj.customer.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer_pk})


class BidDetail(DetailView):
    model = Bid


class BidList(ListView):
    model = Bid


def generate_commercial_invoice(importer_data=None, file_path="output_commercial_invoice.pdf"):

    current_directory = os.path.dirname(os.path.realpath(__file__))

    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import cm
    from reportlab.pdfgen import canvas
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak

    doc = SimpleDocTemplate(file_path, rightMargin=.5 * cm, leftMargin=.5 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()


    story = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Data', alignment=TA_LEFT, fontSize=8, leading=7))
    styles.add(ParagraphStyle(name='Line_Data_Small', alignment=TA_LEFT, fontSize=7, leading=8))
    styles.add(ParagraphStyle(name='Line_Data_Large', alignment=TA_LEFT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Line_Data_Largest', alignment=TA_LEFT, fontSize=14, leading=15))
    styles.add(ParagraphStyle(name='Line_Label', font='Helvetica-Bold', fontSize=7, leading=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Label_Center', font='Helvetica-Bold', fontSize=7, alignment=TA_CENTER))

    address_paragraph = \
        "Jeff Anderson<br />" \
        "670 Ironton ST NE <br />" \
        "Fridley, MN 55432<br />"

    company_paragraph = \
        "Tom Madsen<br />" \
        "179 Marvy ST<br />" \
        "Lino Lakes, MN 55014<br />"

    data1 = [[Paragraph('SHIPPER/EXPORTER (complete name and address)', styles["Line_Label"]),
              Paragraph('CONSIGNEE (complete name and address)', styles["Line_Label"])],

             [Paragraph(address_paragraph, styles["Line_Data_Large"]),
              Paragraph(company_paragraph, styles["Line_Data_Large"])]
             ]

    t1 = Table(data1)
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        ('INNERGRID', (0, 1), (1, 1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(t1)

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)