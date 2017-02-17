from decouple import config
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
import os

from concrete_project import settings
from photo.models import Attachment
from pdf.models import PDFImage


def send_customer_proposal_invoice(pdf_id, body):
    pdf_obj = PDFImage.objects.get(pk=pdf_id)

    if '_proposal_' in pdf_obj.filename.name:
        proposal = True
    else:
        proposal = False

    from_address = config('EMAIL_HOST_USER')
    to_address = pdf_obj.bid.customer.email

    if proposal:
        subject = 'Proposal for {}'.format(pdf_obj.bid.address.street)
    else:
        subject = 'Invoice for {}'.format(pdf_obj.bid.address.street)

    email = EmailMessage(subject, body, from_address, [to_address])

    # Attach PDF
    email.attach_file(pdf_obj.filename.path)

    # If proposal attach bid explanation
    if proposal:
        bid_explanation = os.path.join(settings.MEDIA_ROOT, 'global/bid_explanation.pdf')
        email.attach_file(bid_explanation)

    response = email.send()
    return response


def send_employee_proposal(pdf_id, body):
    attachments = []
    pdf_obj = PDFImage.objects.get(pk=pdf_id)
    attachments.append(pdf_obj)

    photo_objects = Attachment.objects.all().filter(bid=pdf_obj.bid.id)

    for photo_obj in photo_objects:
        attachments.append(photo_obj)

    from_address = config('EMAIL_HOST_USER')
    to_address = pdf_obj.bid.customer.email
    subject = 'Proposal for {}'.format(pdf_obj.bid.address.street)

    email = EmailMessage(subject, body, from_address, [to_address])

    for attachment in attachments:
        email.attach_file(attachment.filename.path)

    response = email.send()

    return response


def send_generic_email():
    pass


class CustomerEmailCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'send_email/send_email_form.html'

    def get_success_url(self):
        messages.success(self.request, "Email Sent Successfully")
        pdf_obj = PDFImage.objects.get(pk=self.kwargs['pdf_id'])
        bid_id = pdf_obj.bid.id
        return reverse('pdf_app:pdf_list', kwargs={'pk': bid_id})

    def form_valid(self, form):
        body = form.cleaned_data['body']
        email_response = send_customer_proposal_invoice(self.kwargs['pdf_id'], body)
        # TODO if email fails to send
        print('Email Response: ', email_response)
        return super(CustomerEmailCreate, self).form_valid(form)

