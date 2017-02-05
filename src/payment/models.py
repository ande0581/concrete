from django.db import models
from django.core.urlresolvers import reverse


class Payment(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=100, blank=True, help_text="Enter Payment Description")
    amount = models.FloatField(max_length=128, blank=True, help_text="Enter Payment Amount")
    bid = models.ForeignKey('bid.Bid', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('bid_app:bid_detail', kwargs={'pk': self.bid.id})
