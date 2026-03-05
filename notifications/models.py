# Create your models here.
from django.db import models

class WorkoutReminder(models.Model):
    RECURRENCE_CHOICES = [
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    user = models.ForeignKey('users.AppUser', on_delete=models.CASCADE)
    plan = models.ForeignKey('workout.WorkoutPlan', on_delete=models.CASCADE, blank=True, null=True)
    reminder_time = models.TimeField()
    recurrence = models.CharField(max_length=20, choices=RECURRENCE_CHOICES, default='once')
    recurrence_days = models.JSONField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'workout_reminders'
