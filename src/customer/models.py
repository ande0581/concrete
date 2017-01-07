from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse


class Customer(models.Model):
    first_name = models.CharField(max_length=64, help_text="Enter the customer's first name")
    last_name = models.CharField(max_length=64, blank=True, help_text="Enter the customer's last name")
    company_name = models.CharField(max_length=128, blank=True, help_text="Enter the company name")
    email = models.EmailField(help_text="Enter the customer email address", blank=True)
    telephone = models.CharField(max_length=10, blank=True, help_text="Enter the customer telephone number")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        if self.company_name:
            return self.company_name
        else:
            return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('customer_app:customer_detail', kwargs={'pk': self.pk})


def customer_model_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.name = instance.first_name.upper()
    instance.name = instance.last_name.upper()
    instance.name = instance.company_name.upper()
    instance.email = instance.email.lower()

pre_save.connect(customer_model_pre_save_receiver, sender=Customer)
