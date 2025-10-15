from django.contrib import admin
from .models import UserProfile, Role, Permission, RolePermission
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','role')
    list_editable = ('role',)
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role',)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role','permission')
    list_filter = ('role',)