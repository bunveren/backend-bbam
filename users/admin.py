from django.contrib import admin
from .models import AppUser, UserProfile, UserDevice

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'height_cm', 'weight_kg')

@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_uuid', 'os_type', 'last_active', 'created_at')
    list_filter = ('os_type',)
    search_fields = ('user__email', 'device_uuid')
    readonly_fields = ('created_at', 'last_active')