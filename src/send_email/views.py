from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
import os

from concrete_project import settings
from pdf.models import PDFImage


def send_customer_email(pdf_id, body):
    pdf_obj = PDFImage.objects.get(pk=pdf_id)
    from_address = 'jeffrey.d.anderson@gmail.com'
    to_address = pdf_obj.bid.customer.email
    subject = 'Proposal for {}'.format(pdf_obj.bid.address.street)
    email = EmailMessage(subject, body, from_address,
                         [to_address])
    filename = os.path.join(settings.MEDIA_ROOT, pdf_obj.filename.name)
    pdf_fh = open(filename, 'rb')
    email.attach(filename, pdf_fh.read(), 'application/pdf')
    response = email.send()
    # response code of 1 success, response code of 0 failure
    return response


class CustomerEmailCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'send_email/send_email_form.html'

    def get_success_url(self):
        messages.success(self.request, "Email Sent Successfully")
        pdf_obj = PDFImage.objects.get(pk=self.kwargs['pdf_id'])
        bid_id = pdf_obj.bid.id
        return reverse('pdf_app:pdf_list', kwargs={'pk': bid_id})

    def form_valid(self, form):
        body = form.cleaned_data['body']
        email_response = send_customer_email(self.kwargs['pdf_id'], body)
        # TODO if email fails to send
        print('Email Response: ', email_response)
        return super(CustomerEmailCreate, self).form_valid(form)

