from django.contrib import admin
from .models import forum_post, forum_comment, bookmarks


@admin.register(forum_post)
class custom_forum_post(admin.ModelAdmin):
    list_display = ('user', 'post_date', 'title')


@admin.register(forum_comment)
class custom_forum_comment(admin.ModelAdmin):
    list_display = ('person', 'comment_date', 'blogs')
