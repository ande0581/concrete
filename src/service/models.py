from django.db import models
from django.core.urlresolvers import reverse


class Service(models.Model):
    description = models.CharField(max_length=200, unique=True)
    cost = models.FloatField()
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE, null=True)
    measurement = models.CharField(max_length=30)
    protected = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('service_app:service_list')
