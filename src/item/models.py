from django.db import models


class BidItem(models.Model):
    bid = models.ForeignKey('bid.Bid', on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    quantity = models.FloatField()
    cost = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return self.description
