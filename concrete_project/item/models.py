from django.db import models

"""
class BidItem(db.Model):

    __tablename__ = "bid_item"

    id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey('bid.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    description = db.Column(db.String)
    quantity = db.Column(db.Float)
    cost = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, bid_id, service_id, description, quantity, cost, total):
        self.bid_id = bid_id
        self.service_id = service_id
        self.description = description
        self.quantity = quantity
        self.cost = cost
        self.total = total

    def __repr__(self):
        return '<{}>'.format(self.description)
"""


class BidItem(models.Model):
    bid_id = models.ForeignKey('bid.Bid', on_delete=models.CASCADE)
    service_id = models.ForeignKey('service.Service', on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    quantity = models.FloatField()
    cost = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return self.description
