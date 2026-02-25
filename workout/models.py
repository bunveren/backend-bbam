from django.db import models
from django.utils import timezone

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    gif_url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'exercises'

    def __str__(self):
        return self.name


class ExerciseRule(models.Model):
    exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE)
    rules_json = models.JSONField()
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'exercise_rules'


class WorkoutPlan(models.Model):
    user = models.ForeignKey('users.AppUser', on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'workout_plans'

    def __str__(self):
        return self.plan_name
    
    def delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
    
    @property
    def is_deleted(self):
        return self.deleted_at is not None


class WorkoutPlanItem(models.Model):
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    step_order = models.IntegerField()
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    target_reps = models.IntegerField(blank=True, null=True)
    target_seconds = models.IntegerField(blank=True, null=True)
    set_label = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'workout_plan_items'
        unique_together = (('plan', 'step_order'),)
        indexes = [models.Index(fields=['plan', 'step_order'], name='idx_plan_items_plan_order')]