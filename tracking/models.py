from django.db import models
from django.contrib.postgres.indexes import GinIndex

class WorkoutSession(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey('users.AppUser', on_delete=models.CASCADE)
    plan = models.ForeignKey('workout.WorkoutPlan', on_delete=models.SET_NULL, blank=True, null=True)
    
    plan_name = models.CharField(max_length=255, blank=True, null=True)
    session_date = models.DateField()
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    overall_accuracy_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'workout_sessions'
        indexes = [models.Index(fields=['user', '-session_date'], name='idx_sessions_user_date'),]

    def __str__(self):
        return f"{self.user} - {self.session_date} ({self.status})"


class SessionExercise(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    exercise = models.ForeignKey('workout.Exercise', on_delete=models.PROTECT)
    
    step_order = models.IntegerField()
    target_reps = models.IntegerField(blank=True, null=True)
    target_seconds = models.IntegerField(blank=True, null=True)
    
    completed_reps = models.IntegerField(blank=True, null=True)
    completed_seconds = models.IntegerField(blank=True, null=True)
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    common_errors = models.JSONField(blank=True, null=True)
    #feedback_summary = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'session_exercises'
        unique_together = (('session', 'step_order'),)


class SessionSummary(models.Model):
    session = models.OneToOneField(WorkoutSession, on_delete=models.CASCADE, primary_key=True)
    summary_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'session_summaries'
        indexes = [GinIndex(fields=['summary_json'], name='idx_summary_json'),]