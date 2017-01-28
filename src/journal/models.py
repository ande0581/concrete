from django.db import models
from django.urls import reverse


class Journal(models.Model):
    body = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    bid = models.ForeignKey('bid.Bid', on_delete=models.CASCADE)

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('bid_app:bid_update', kwargs={'pk': self.bid.id})
