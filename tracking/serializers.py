from rest_framework import serializers
from .models import WorkoutSession, SessionExercise, SessionSummary

class SessionExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionExercise
        fields = '__all__'

class SessionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionSummary
        fields = '__all__'

class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'
        read_only_fields = ['user']