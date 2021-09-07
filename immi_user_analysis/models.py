from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.crypto import get_random_string


class UserTask(models.Model):

    task_name = models.CharField(max_length=255)
    task_url = models.SlugField(blank=True, null=True)
    task_creation_date = models.DateTimeField(auto_now_add=True)
    task_description = RichTextUploadingField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.task_url:
            self.task_url = slugify(self.task_name + '-' + get_random_string(length=4))
        else:
            self.task_url = slugify(self.task_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/tasks/{self.task_url}/'

    def task_snippet(self):
        return self.task_description[:150]

    def __str__(self):
        return self.task_name


class UserTaskStatus(models.Model):
    task = models.ForeignKey(UserTask, related_name="prospective_student_tasks_list", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="prospective_student_tasks", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} completed by {self.user}"
