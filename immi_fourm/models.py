from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class ForumPost(models.Model):
    user = models.ForeignKey(User, related_name="forum_author", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    post_url = models.SlugField(null=True, blank=True)
    post_description = models.TextField(max_length=1500)
    like = models.ManyToManyField(User, related_name="blogs_post")
    post_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.post_url:
            self.post_url = slugify(f"{self.title} - {get_random_string(length=4)}")
        else:
            self.post_url = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/forum/{self.post_url}/"

    def total_likes(self):
        return self.like

    def __str__(self):
        return self.title


class ForumComment(models.Model):
    blogs = models.ForeignKey(ForumPost, related_name="forum_comments", on_delete=models.CASCADE)
    person = models.ForeignKey(User, related_name="forum_comments_user", on_delete=models.CASCADE)
    comment_body = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    all_like = models.ManyToManyField(User, related_name="comment_like")

    def total_comment_likes(self):
        return self.all_like

    def __str__(self):
        return self.blogs


class AllBookmark(models.Model):
    blogs = models.ForeignKey(ForumPost, related_name="bookmarks_blogs", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="bookmarks_user", on_delete=models.CASCADE)
