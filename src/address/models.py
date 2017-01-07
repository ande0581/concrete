from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse


class Address(models.Model):

    street = models.CharField(max_length=128, blank=True, help_text="Enter the street address")
    city = models.CharField(max_length=50, blank=True, help_text="Enter the city")
    state = models.CharField(max_length=2, blank=True, help_text="Enter the 2 digit state abbreviation")
    zip = models.CharField(max_length=5, blank=True, help_text="Enter the 5 digit zipcode")
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(self.street, self.city, self.state, self.zip)

    def get_absolute_url(self):
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer.id})


def address_model_pre_save_receiver(sender, instance, *args, **kwargs):
        instance.street = instance.street.upper()
        instance.city = instance.city.upper()
        instance.state = instance.state.upper()

pre_save.connect(address_model_pre_save_receiver, sender=Address)
