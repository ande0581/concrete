from django.db import models
from django.core.urlresolvers import reverse

BID_STATUS = [
    ('Needs Bid', 'Needs Bid'), ('Awaiting Customer Acceptance', 'Awaiting Customer Acceptance'),
    ('Job Accepted', 'Job Accepted'), ('Job Started', 'Job Started'), ('Job Completed', 'Job Completed'),
    ('Job Declined', 'Job Declined')
    ]


class Bid(models.Model):
    description = models.CharField(max_length=2000)
    notes = models.CharField(max_length=2000, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    address = models.ForeignKey('address.Address')
    scheduled_bid_date = models.DateTimeField(null=True, blank=True)
    tentative_start = models.DateField(null=True, blank=True)
    actual_start = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    down_payment_amount = models.FloatField(default=0)
    down_payment_date = models.DateField(null=True, blank=True)
    final_payment_amount = models.FloatField(default=0)
    final_payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=2000, choices=BID_STATUS, default='Needs Bid')

    class Meta:
        verbose_name_plural = 'Bids'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('bid_app:bid_update', kwargs={'pk': self.id})
