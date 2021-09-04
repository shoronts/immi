from django.contrib import admin
from .models import single_message, groups_list, group_message


@admin.register(single_message)
class custom_single_message(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'date')


@admin.register(groups_list)
class custom_groups_list(admin.ModelAdmin):
    list_display = ('group_name',)


@admin.register(group_message)
class custom_group_message(admin.ModelAdmin):
    list_display = ('group', 'date', 'sender', 'message')
