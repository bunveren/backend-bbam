from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Exercise, ExerciseRule, WorkoutPlan, WorkoutPlan
from .serializers import (
    ExerciseSerializer, ExerciseRuleSerializer, 
    WorkoutPlanSerializer
)
from .services import ExerciseLibraryService
from rest_framework import status
from rest_framework.decorators import action

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class WorkoutController(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    def list_exercises(self, request):
        exercises = ExerciseLibraryService.get_all_exercises()
        return Response(exercises)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExerciseLibraryViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ExerciseRuleViewSet(viewsets.ModelViewSet):
    queryset = ExerciseRule.objects.all()
    serializer_class = ExerciseRuleSerializer
    
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user, deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)