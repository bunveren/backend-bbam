from rest_framework import serializers
from .models import Exercise, ExerciseRule, WorkoutPlan, WorkoutPlanItem

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class ExerciseRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRule
        fields = '__all__'

class WorkoutPlanItemSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(), source='exercise', write_only=True
    )

    class Meta:
        model = WorkoutPlanItem
        fields = ['id', 'exercise', 'exercise_id', 'step_order', 'target_reps', 'target_seconds', 'set_label']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    items = WorkoutPlanItemSerializer(many=True, source='workoutplanitem_set')
    
    class Meta:
        model = WorkoutPlan
        fields = ['id', 'user', 'plan_name', 'items', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        items_data = validated_data.pop('workoutplanitem_set', [])
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        for item_data in items_data:
            WorkoutPlanItem.objects.create(plan=workout_plan, **item_data)
        return workout_plan
