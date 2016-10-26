from django.db import models

"""
class Service(db.Model):

    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    cost = db.Column(db.Float)

    def __init__(self, description, cost):
        self.description = description
        self.cost = cost

    def __repr__(self):
        return '<{}>'.format(self.description)
"""


class Service(models.Model):
    description = models.CharField(max_length=200)
    cost = models.FloatField()

    def __str__(self):
        return self.description
