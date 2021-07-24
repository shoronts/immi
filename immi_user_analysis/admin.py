from django.contrib import admin
from .models import users_task, user_task_status


admin.site.register(users_task)
admin.site.register(user_task_status)
