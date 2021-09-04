from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from .models import UserInfo


admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name','username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_display_links = ('username',)

@admin.register(UserInfo)
class CustomUserInfo(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'nationality', 'program')
    list_display_links = ('user',)
