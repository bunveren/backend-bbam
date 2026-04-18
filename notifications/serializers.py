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
    
    def validate(self, data):
        request = self.context.get('request')
        provided_user_id = request.data.get('user')

        if provided_user_id and int(provided_user_id) != request.user.id:
            raise serializers.ValidationError(
                {"user": "You cannot create a reminder for another user."}
            )
        return data
    
    def validate_plan(self, value):
        request = self.context.get('request')
        user = request.user

        if value is not None:
            if value.user != user:
                raise serializers.ValidationError(
                    "You cannot link a reminder to a plan that doesn't belong to you."
                )
            
            if value.is_deleted: 
                raise serializers.ValidationError(
                    "You cannot link a reminder to this plan."
                )
        return value