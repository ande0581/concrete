from django.db import models

"""
class Journal(db.Model):
    __tablename__ = "journal"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __init__(self, body, timestamp, customer_id):
        self.body = body
        self.timestamp = timestamp
        self.customer_id = customer_id

    def __repr__(self):
        return '<{}>'.format(self.post)
"""


class Journal(models.Model):
    body = models.CharField(max_length=2000)
    timestamp = models.DateTimeField()
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)

    def __str__(self):
        return self.body
