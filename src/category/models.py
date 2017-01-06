from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('category_app:category_list')
