from django.db import models
from django.core.urlresolvers import reverse

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

CATEGORIES = [
    ('concrete', 'concrete'),
    ('rebar', 'rebar'),
    ('stamp', 'stamp')
]


class Service(models.Model):
    description = models.CharField(max_length=200)
    cost = models.FloatField()
    category = models.CharField(max_length=2000, choices=CATEGORIES, default='No Category')
    protected = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('service_app:service_list')
