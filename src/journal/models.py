from django.db import models


class Journal(models.Model):
    body = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)

    def __str__(self):
        return self.body
