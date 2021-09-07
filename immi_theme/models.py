from django.db import models


class Notification(models.Model):
    name = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    held_by = models.CharField(max_length=255)
    view = models.BooleanField(default=False)
    notification = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
