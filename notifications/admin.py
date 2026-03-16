from django.contrib import admin
from .models import WorkoutReminder

@admin.register(WorkoutReminder)
class WorkoutReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'reminder_time', 'recurrence', 'is_active', 'created_at')
    list_filter = ('recurrence', 'is_active')
    search_fields = ('user__email', 'message')
    readonly_fields = ('created_at', 'updated_at')