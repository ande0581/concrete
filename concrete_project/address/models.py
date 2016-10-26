from django.db import models

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

    street = models.CharField(max_length=128)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=25)
    zip = models.CharField(max_length=10)
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    # address_bids

    def __str__(self):
        return self.street
