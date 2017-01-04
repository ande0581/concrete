from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

"""
class Address(db.Model):

    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    address_bids = db.relationship('Bid', backref='address_bid', cascade="all, delete-orphan", lazy='joined')

    def __init__(self, street, city, state, zip, customer_id):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.customer_id = customer_id

    def __repr__(self):
        return '<{0}, {1}, {2}, {3}>'.format(self.street, self.city, self.state, self.zip)
"""


class Address(models.Model):

    street = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=5, blank=True)
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(self.street, self.city, self.state, self.zip)

    def get_absolute_url(self):
        return reverse('customer_app:customer_detail', kwargs={'pk': self.customer_id.id})


def address_model_pre_save_receiver(sender, instance, *args, **kwargs):
        instance.street = instance.street.upper()
        instance.city = instance.city.upper()
        instance.state = instance.state.upper()

pre_save.connect(address_model_pre_save_receiver, sender=Address)
