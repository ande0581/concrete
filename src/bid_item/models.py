from django.db import models
from django.core.urlresolvers import reverse


class BidItem(models.Model):

    bid = models.ForeignKey('bid.Bid', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    quantity = models.FloatField(null=True)
    cost = models.FloatField(null=True)
    total = models.FloatField()

    class Meta:
        verbose_name_plural = 'BidItems'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('bid_app:bid_update', kwargs={'pk': self.bid.id})
