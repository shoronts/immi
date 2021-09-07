from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Notification


admin.site.unregister(Group)
admin.site.site_header = 'Immu admin Dashboard'
admin.site.site_title = 'Immu'
admin.site.index_title = 'Immu Administration'


@admin.register(Notification)
class CustomNotification(admin.ModelAdmin):
    list_display = ('date', 'name', 'user', 'held_by', 'view', 'notification')
