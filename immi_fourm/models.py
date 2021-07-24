from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class forum_post(models.Model):
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    post_url = models.SlugField(null=False)
    post_images = models.ImageField(upload_to='blogs_pics', blank = False, null = False)
    post_discription = models.TextField(max_length=1500)
    like = models.ManyToManyField(User, related_name="blogs_post")
    post_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.post_url:
            self.post_url = slugify(self.title + get_random_string(length=4))
        else:
            self.post_url = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/forum/{self.forum_url}/'

    def total_likes(self):
        return self.like.count()

    def snippet(self):
        return self.post_discription[:250] + ' .....'

    def snippet_title(self):
        return self.title[:20] + ' ...'

    def __str__(self):
        return self.title

class forum_comment(models.Model):
    blogs = models.ForeignKey(forum_post, related_name="forum_comments", on_delete=models.CASCADE)
    person = models.ForeignKey(User, related_name="forum_comments_user", on_delete=models.CASCADE)
    comment_body = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blogs.title
