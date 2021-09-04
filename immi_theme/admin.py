from django.contrib import admin
from django.contrib.auth.models import Group
from .models import notification


admin.site.unregister(Group)
admin.site.site_header = 'Immu admin Dashboard'
admin.site.site_title = 'Immu'
admin.site.index_title = 'Immu Administration'

admin.site.register(notification)
