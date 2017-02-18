from django.db import models
from django.urls import reverse


class EmailLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    to_address = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    body = models.CharField(max_length=2000)
    successful = models.BooleanField()
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer.id})
