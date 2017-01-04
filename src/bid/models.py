from django.db import models
from django.core.urlresolvers import reverse

"""
class Bid(db.Model):

    __tablename__ = "bid"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    notes = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    scheduled_bid_date = db.Column(db.DateTime)
    tentative_start = db.Column(db.Date)
    actual_start = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    down_payment_amount = db.Column(db.Float, default=0)
    down_payment_date = db.Column(db.Date)
    final_payment_amount = db.Column(db.Float, default=0)
    final_payment_date = db.Column(db.Date)
    status = db.Column(db.String)
    bid_items = db.relationship('BidItem', backref='bid_item', cascade="all, delete-orphan", lazy='joined')

    def __init__(self, description, notes, timestamp, customer_id, address_id, scheduled_bid_date, tentative_start,
                 actual_start, completion_date, down_payment_amount, down_payment_date, final_payment_amount,
                 final_payment_date, status):
        self.description = description
        self.notes = notes
        self.timestamp = timestamp
        self.customer_id = customer_id
        self.address_id = address_id
        self.scheduled_bid_date = scheduled_bid_date
        self.tentative_start = tentative_start
        self.actual_start = actual_start
        self.completion_date = completion_date
        self.down_payment_amount = down_payment_amount
        self.down_payment_date = down_payment_date
        self.final_payment_amount = final_payment_amount
        self.final_payment_date = final_payment_date
        self.status = status

    def __repr__(self):
        return '<{}>'.format(self.description)
"""

BID_STATUS = [
    ('Needs Bid', 'Needs Bid'), ('Awaiting Customer Acceptance', 'Awaiting Customer Acceptance'),
    ('Job Accepted', 'Job Accepted'), ('Job Started', 'Job Started'), ('Job Completed', 'Job Completed'),
    ('Job Declined', 'Job Declined')
    ]


class Bid(models.Model):
    description = models.CharField(max_length=2000)
    notes = models.CharField(max_length=2000, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    address_id = models.ForeignKey('address.Address')
    scheduled_bid_date = models.DateTimeField(null=True)
    tentative_start = models.DateField(null=True)
    actual_start = models.DateField(null=True)
    completion_date = models.DateField(null=True)
    down_payment_amount = models.FloatField(default=0)
    down_payment_date = models.DateField(null=True)
    final_payment_amount = models.FloatField(default=0)
    final_payment_date = models.DateField(null=True)
    status = models.CharField(max_length=2000, choices=BID_STATUS, default='Needs Bid')

    class Meta:
        verbose_name_plural = 'Bids'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('customer_app:customer_detail', kwargs={'pk': int(self.customer_id)})
