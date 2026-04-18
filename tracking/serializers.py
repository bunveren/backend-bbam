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
    summary_json = serializers.SerializerMethodField()
    class Meta:
        model = WorkoutSession
        fields = '__all__'
        read_only_fields = ['user']

    def get_summary_json(self, obj):
        # Access the related SessionSummary object
        summary = SessionSummary.objects.filter(session=obj).first()
        return summary.summary_json if summary else None