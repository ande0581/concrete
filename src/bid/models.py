from django.db import models
from django.db.models.signals import pre_save
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
    custom_down_payment = models.FloatField(null=True, blank=True,
                                            verbose_name='Custom Down Payment: Entering 0 means no down payment, leave blank for standard down payment, or enter custom value')
    status = models.CharField(max_length=2000, choices=BID_STATUS, default='Needs Bid')
    billto_name = models.CharField(max_length=100, blank=True, verbose_name='Alternative Bill To Name')
    billto_street = models.CharField(max_length=100, blank=True, verbose_name='Alternative Bill To Street')
    billto_city_st_zip = models.CharField(max_length=100, blank=True, verbose_name="Alternative Bill To City, ST, ZIP")
    billto_telephone = models.CharField(max_length=10, blank=True, verbose_name="Alternative Bill To Telephone Number")

    class Meta:
        verbose_name_plural = 'Bids'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('bid_app:bid_detail', kwargs={'pk': self.id})


def bid_model_pre_save_receiver(sender, instance, *args, **kwargs):
        instance.billto_name = instance.billto_name.upper()
        instance.billto_street = instance.billto_street.upper()
        instance.billto_city_st_zip = instance.billto_city_st_zip.upper()


pre_save.connect(bid_model_pre_save_receiver, sender=Bid)
