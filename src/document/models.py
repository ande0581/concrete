from django.db import models
from django.urls import reverse


def generate_filename(instance, filename):

    url = "global/{}".format(filename)

    return url


class Document(models.Model):

    description = models.CharField(max_length=100)
    filename = models.FileField(upload_to=generate_filename)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('document_app:document_list')

    def __str__(self):
        return self.description

    def shorten_filename(self):
        folder1, filename = self.filename.name.split('/')
        return filename