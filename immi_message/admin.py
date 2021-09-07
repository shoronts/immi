from django.contrib import admin
from .models import SingleMessage, GroupMessage, GroupsList


@admin.register(SingleMessage)
class CustomSingleMessage(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'date')


@admin.register(GroupsList)
class CustomGroupsList(admin.ModelAdmin):
    list_display = ('group_name',)


@admin.register(GroupMessage)
class CustomGroupMessage(admin.ModelAdmin):
    list_display = ('group', 'date', 'sender', 'message')
