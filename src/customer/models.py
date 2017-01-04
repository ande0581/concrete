from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

"""
class Customer(db.Model):

    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    telephone = db.Column(db.String, nullable=False)
    created_date = db.Column(db.Date, default=datetime.datetime.now(pytz.timezone('US/Central')))
    addresses = db.relationship('Address', backref='customer', cascade="all, delete-orphan", lazy='joined')
    journals = db.relationship('Journal', backref='journal', cascade="all, delete-orphan", lazy='joined')
    customer_bids = db.relationship('Bid', backref='customer_bid', cascade="all, delete-orphan", lazy='joined')

    def __init__(self, name, email, telephone, created_date):
        self.name = name
        self.email = email
        self.telephone = telephone
        self.created_date = created_date

    def __repr__(self):
        return '<name {0}>'.format(self.name)
"""


class Customer(models.Model):
    # TODO Change name to first, last and add company
    first_name = models.CharField(max_length=64, help_text="Enter the customer's first name")
    last_name = models.CharField(max_length=64, blank=True, help_text="Enter the customer's last name")
    company_name = models.CharField(max_length=128, blank=True, help_text="Enter the company name")
    email = models.EmailField(help_text="Enter the customer email address")
    telephone = models.CharField(max_length=10, help_text="Enter the customer telephone number")
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
