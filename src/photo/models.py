from django.db import models


class Attachment(models.Model):
    # TODO add foreignkey and date to model
    file = models.FileField(upload_to='attachments')