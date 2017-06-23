from django.db import models
from django.urls import reverse
import datetime


def generate_filename(instance, pdf_type):

    name = instance.bid.customer.__str__().replace(' ', '_').lower()
    folder = "{}_{}".format(name, instance.bid.customer.id)
    filename = "{}_{}_{}.pdf".format(name, pdf_type, datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))
    url = "customers/{}/{}".format(folder, filename)

    return url


class PDFImage(models.Model):

    bid = models.ForeignKey('bid.bid', on_delete=models.CASCADE)
    filename = models.FileField(upload_to=generate_filename)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('pdf_app:pdf_list', kwargs={'pk': self.bid_id})

    def __str__(self):
        return str(self.filename)

    def shorten_filename(self):
        folder1, folder2, filename = self.filename.name.split('/')
        return filename





