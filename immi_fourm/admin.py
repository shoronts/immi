from django.contrib import admin
from .models import forum_post, forum_comment


admin.site.register(forum_post)
admin.site.register(forum_comment)
