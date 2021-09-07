from django.contrib import admin
from .models import ForumPost, ForumComment, AllBookmark


@admin.register(ForumPost)
class CustomForumPost(admin.ModelAdmin):
    list_display = ('user', 'post_date', 'title')


@admin.register(ForumComment)
class CustomForumComment(admin.ModelAdmin):
    list_display = ('person', 'comment_date', 'blogs')


@admin.register(AllBookmark)
class CustomAllBookmak(admin.ModelAdmin):
    list_display = ('user', 'blogs')

