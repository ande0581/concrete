from django.db import models
import datetime
import os

from django.urls import reverse


def generate_filename(instance, filename):

    fname, ext = os.path.splitext(filename)

    customer = instance.bid.customer.__str__().replace(' ', '_').lower()
    folder = "{}_{}".format(customer, instance.bid.customer.id)
    new_fname = "{}_{}{}".format(fname, datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'), ext)
    url = "customers/{}/{}".format(folder, new_fname)

    return url


class Attachment(models.Model):

    bid = models.ForeignKey('bid.bid')
    filename = models.FileField(upload_to=generate_filename)

    def get_absolute_url(self):
        return reverse('photo_app:photo_list', kwargs={'bid_id': self.bid.id})
