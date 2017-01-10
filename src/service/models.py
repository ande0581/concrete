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


class Service(models.Model):
    description = models.CharField(max_length=200, unique=True)
    cost = models.FloatField()
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('service_app:service_list')
