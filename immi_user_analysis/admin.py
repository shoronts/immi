from django.contrib import admin
from .models import users_task


@admin.register(users_task)
class custom_users_task(admin.ModelAdmin):
    list_display = ('task_name', 'task_creation_date')
