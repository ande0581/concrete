from django.db import models
import datetime

from django.urls import reverse


def generate_filename(instance, _blank):

    name = instance.bid.customer.__str__().replace(' ', '_').lower()
    folder = "{}_{}".format(name, instance.bid.customer.id)
    filename = "{}_{}.pdf".format(name, datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))
    url = "customers/{}/{}".format(folder, filename)

    return url


class PDFImage(models.Model):

    bid = models.ForeignKey('bid.bid', on_delete=models.CASCADE)
    filename = models.FileField(upload_to=generate_filename)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('pdf_app:pdf_list', kwargs={'pk': self.bid.id})

