from django.db import models
from django.core.urlresolvers import reverse


class JobType(models.Model):
    description = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('job_type_app:job_type_list')
