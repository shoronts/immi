from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class SingleMessage(models.Model):
    sender = models.CharField( max_length=255)
    receiver = models.CharField( max_length=255)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} message to {self.receiver}"


class GroupsList(models.Model):
    group_name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    group_member = models.ManyToManyField(User, related_name="group_members_list")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.CharField( max_length=255)
    sender = models.CharField( max_length=255)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} send this message to group"
