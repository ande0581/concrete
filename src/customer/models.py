from django.db import models
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
    name = models.CharField(max_length=128)
    email = models.EmailField(null=False)
    telephone = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __int__(self):
        # this is required to create an address for the redirect on successful ??
        # TODO figure out why this is required
        return self.pk

    def get_absolute_url(self):
        return reverse('customer_app:customer_detail', kwargs={'pk': self.pk})
