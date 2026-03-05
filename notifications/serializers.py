from rest_framework import serializers
from .models import WorkoutReminder

class WorkoutReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutReminder
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_recurrence_days(self, value):
        if value is not None and not isinstance(value, list):
            raise serializers.ValidationError("recurrence_days needs to be an array.")
        return value
    