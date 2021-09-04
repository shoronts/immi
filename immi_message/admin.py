from django.contrib import admin
from .models import single_message, groups_list, group_message


admin.site.register(single_message)
admin.site.register(groups_list)
admin.site.register(group_message)
