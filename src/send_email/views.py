import datetime
from decouple import config
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
import os

from concrete_project import settings
from bid.models import Bid
from customer.models import Customer
from photo.models import Attachment
from pdf.models import PDFImage
from send_email.models import EmailLog
from pdf.views import view_pdf


def generate_filename(instance):
    name = instance.customer.__str__().replace(' ', '_').lower()
    filename = "{}_Employee_Copy_{}.pdf".format(name, datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))

    return filename


def log_email(**kwargs):
    customer_obj = Customer.objects.get(pk=kwargs['customer_id'])

    email_entry = EmailLog()
    email_entry.to_address = kwargs['to_address']
    email_entry.subject = kwargs['subject']
    email_entry.body = kwargs['body']
    email_entry.successful = kwargs['successful']
    email_entry.customer = customer_obj
    email_entry.save()


def send_customer_proposal_invoice_email(pdf_id, body, attachments):
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
        body = body.replace('proposal', 'invoice')

    email = EmailMessage(subject, body, from_address, [to_address])

    # Attach PDF
    email.attach_file(pdf_obj.filename.path)

    # If proposal attach supporting documents
    if proposal:
        media_folder = os.path.join(settings.MEDIA_ROOT, 'global')
        bid_explanation = os.path.join(media_folder, 'bid_explanation.pdf')
        liabilities_warranty = os.path.join(media_folder, 'liabilities_warranty.pdf')
        what_to_expect = os.path.join(media_folder, 'what_to_expect.pdf')
        contractor_license = os.path.join(media_folder, 'contractor_license.pdf')
        email.attach_file(bid_explanation)
        email.attach_file(liabilities_warranty)
        email.attach_file(what_to_expect)
        email.attach_file(contractor_license)

    # Add any additional attachments selected on form submission
    for attachment in attachments:
        email.attach_file(attachment.filename.path)

    # Attempt to send email
    try:
        response = email.send()
    except Exception:
        response = 0

    # Log email in DB
    email_log_entry = {
        'to_address': to_address,
        'subject': subject,
        'body': body,
        'successful': response,
        'customer_id': pdf_obj.bid.customer.id
    }

    log_email(**email_log_entry)

    return response


def send_employee_bid_email(request, bid_id, to_address, body):
    attachments = []
    bid_obj = Bid.objects.get(pk=bid_id)
    pdf_name = generate_filename(bid_obj)

    from_address = config('EMAIL_HOST_USER')
    subject = 'Job Details for {}'.format(bid_obj.address.street)

    email = EmailMessage(subject, body, from_address, [to_address])

    # Generate PDF to attach to email
    employee_pdf = view_pdf(request, invoice=False, employee=True, bid_id=bid_id, return_file_object=True)
    email.attach(pdf_name, content=employee_pdf, mimetype='application/pdf')

    # Collect photos from bid to attach to email
    photo_objects = Attachment.objects.all().filter(bid=bid_obj.id)

    for photo_obj in photo_objects:
        attachments.append(photo_obj)

    for attachment in attachments:
        email.attach_file(attachment.filename.path)

    # Attempt to send email
    try:
        response = email.send()
    except Exception:
        response = 0

    # Log email in DB
    email_log_entry = {
        'to_address': to_address,
        'subject': subject,
        'body': body,
        'successful': response,
        'customer_id': bid_obj.customer.id
    }

    log_email(**email_log_entry)

    return response


def send_general_email(customer_id, to_address, subject, body, attachments):
    customer_obj = Customer.objects.get(pk=customer_id)
    from_address = config('EMAIL_HOST_USER')
    email = EmailMessage(subject, body, from_address, [to_address])

    # Add any additional attachments selected on form submission
    for attachment in attachments:
        email.attach_file(attachment.filename.path)

    # Attempt to send email
    try:
        response = email.send()
    except Exception:
        response = 0

    # Log email in DB
    email_log_entry = {
        'to_address': to_address,
        'subject': subject,
        'body': body,
        'successful': response,
        'customer_id': customer_obj.id
    }

    log_email(**email_log_entry)

    return response


class EmployeeEmailCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'send_email/send_email_form.html'

    def get_success_url(self):
        bid_obj = Bid.objects.get(pk=self.kwargs['bid_id'])
        return reverse('bid_app:bid_detail', kwargs={'pk': bid_obj.id})

    def form_valid(self, form):
        body = form.cleaned_data['body']
        to_address = form.cleaned_data['to_address']
        email_response = send_employee_bid_email(self.request, self.kwargs['bid_id'], to_address, body)
        if email_response:
            messages.success(self.request, 'Successfully sent email to {}'.format(to_address))
        else:
            messages.error(self.request, 'Failed to send email to {}'.format(to_address))
        return super(EmployeeEmailCreate, self).form_valid(form)


class ProposalInvoiceEmailCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'send_email/send_email_form.html'

    def get_success_url(self):
        pdf_obj = PDFImage.objects.get(pk=self.kwargs['pdf_id'])
        bid_id = pdf_obj.bid.id
        return reverse('bid_app:bid_detail', kwargs={'pk': bid_id})

    def form_valid(self, form):
        body = form.cleaned_data['body']
        pdf_obj = PDFImage.objects.get(pk=self.kwargs['pdf_id'])
        attachments = form.cleaned_data['attachments']
        to_address = pdf_obj.bid.customer.email
        email_response = send_customer_proposal_invoice_email(self.kwargs['pdf_id'], body, attachments)
        if email_response:
            messages.success(self.request, 'Successfully sent email to {}'.format(to_address))
        else:
            messages.error(self.request, 'Failed to send email to {}'.format(to_address))
        return super(ProposalInvoiceEmailCreate, self).form_valid(form)


class GeneralEmailCreate(LoginRequiredMixin, FormView):

    template_name = 'send_email/send_email_form.html'

    def get_success_url(self):
        customer_obj = Customer.objects.get(pk=self.kwargs['customer_id'])
        return reverse('customer_app:customer_detail', kwargs={'pk': customer_obj.id})

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        body = form.cleaned_data['body']
        attachments = form.cleaned_data['attachments']
        customer_obj = Customer.objects.get(pk=self.kwargs['customer_id'])
        to_address = customer_obj.email
        email_response = send_general_email(customer_obj.id, to_address, subject, body, attachments)
        if email_response:
            messages.success(self.request, 'Successfully sent email to {}'.format(to_address))
        else:
            messages.error(self.request, 'Failed to send email to {}'.format(to_address))

        return super(GeneralEmailCreate, self).form_valid(form)

