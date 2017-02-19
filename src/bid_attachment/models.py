from django.db import models
from django.urls import reverse


def generate_filename(instance, filename):

    customer = instance.bid.customer.__str__().replace(' ', '_').lower()
    folder = "{}_{}".format(customer, instance.bid.customer.id)
    url = "customers/{}/{}".format(folder, filename)

    return url


class Document(models.Model):

    bid = models.ForeignKey('bid.bid')
    description = models.CharField(max_length=100)
    filename = models.FileField(upload_to=generate_filename)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('bid_attachment_app:bid_attachment_list', kwargs={'bid_id': self.bid.id})

    def __str__(self):
        return self.description

    def shorten_filename(self):
        folder1, folder2, filename = self.filename.name.split('/')
        return filename
