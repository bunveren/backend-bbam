from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Exercise, ExerciseRule, WorkoutPlan, WorkoutReminder, WorkoutPlan
from .serializers import (
    ExerciseSerializer, ExerciseRuleSerializer, 
    WorkoutPlanSerializer, WorkoutReminderSerializer
)
from .services import ExerciseLibraryService
from notifications.services import NotificationService

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
"""
class WorkoutReminderViewSet(viewsets.ModelViewSet):
    queryset = WorkoutReminder.objects.all()
    serializer_class = WorkoutReminderSerializer
"""

class WorkoutController(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    def list_exercises(self, request):
        exercises = ExerciseLibraryService.get_all_exercises()
        return Response(exercises)

    def create_workout_plan(self, request):
        pass #todo ins mas

class ExerciseLibraryViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ExerciseRuleViewSet(viewsets.ModelViewSet):
    queryset = ExerciseRule.objects.all()
    serializer_class = ExerciseRuleSerializer

class NotificationController(viewsets.ModelViewSet):
    queryset = WorkoutReminder.objects.all()
    serializer_class = WorkoutReminderSerializer
    
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutPlan.objects.filter(created_by=self.request.user, deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutReminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        reminder = serializer.save(user=self.request.user)
        try:
            NotificationService.send_sync_signal(self.request.user)
        except Exception as e:
            print(f"Sync signal error: {e}")