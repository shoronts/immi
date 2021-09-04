from django.contrib import admin
from .models import forum_post, forum_comment, bookmarks


admin.site.register(forum_post)
admin.site.register(forum_comment)
