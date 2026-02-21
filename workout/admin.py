from django.contrib import admin
from .models import Exercise, ExerciseRule, WorkoutPlan, WorkoutPlanItem, WorkoutReminder

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(ExerciseRule)
class ExerciseRuleAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'is_active')

class WorkoutPlanItemInline(admin.TabularInline):
    model = WorkoutPlanItem
    extra = 1

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'user', 'created_at')
    inlines = [WorkoutPlanItemInline]

@admin.register(WorkoutReminder)
class WorkoutReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'reminder_time', 'recurrence', 'is_active', 'created_at', 'updated_at')