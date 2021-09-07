from django.contrib import admin
from .models import UserTask


@admin.register(UserTask)
class CustomUsersTask(admin.ModelAdmin):
    list_display = ('task_name', 'task_creation_date')
