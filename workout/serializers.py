from rest_framework import serializers
from .models import Exercise, ExerciseRule, WorkoutPlan, WorkoutPlanItem
from django.utils import timezone
from django.db import transaction

class ExerciseSerializer(serializers.ModelSerializer):
    rules_json = serializers.SerializerMethodField()
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'gif_url', 'created_at', 'rules_json']
    
    def get_rules_json(self, obj):
        try:
            if hasattr(obj, 'exerciserule') and obj.exerciserule.is_active:
                return obj.exerciserule.rules_json
        except Exception:
            return None
        return None

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

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        if items_data is None:
            items_data = validated_data.pop('workoutplanitem_set', None)
        if items_data is not None:
            with transaction.atomic():
                new_plan_name = validated_data.get('plan_name', instance.plan_name)
                new_plan = WorkoutPlan.objects.create(
                    user=instance.user,
                    plan_name=new_plan_name,
                )
                
                for item_data in items_data: WorkoutPlanItem.objects.create(plan=new_plan, **item_data)
                instance.deleted_at = timezone.now()
                instance.save()
                return new_plan
        
        else:
            for attr, value in validated_data.items(): setattr(instance, attr, value)
            instance.save()
            return instance