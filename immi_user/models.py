from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100)
    profilepic = models.ImageField(default='profile-pic.svg', upload_to='Users_Profile_pic')

    def __str__(self):
        return self.user.username
