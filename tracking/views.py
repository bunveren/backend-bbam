from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WorkoutSession, SessionExercise, SessionSummary
from .serializers import (
    WorkoutSessionSerializer, SessionExerciseSerializer, SessionSummarySerializer
)
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from tracking.services import PerformanceAnalyzer

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'])
    def log_exercise(self, request, pk=None):
        session = self.get_object()
        data = request.data
        
        SessionExercise.objects.create(
            session=session,
            exercise_id=data.get('exercise_id'),
            completed_reps=data.get('completed_reps'),
            accuracy_score=data.get('accuracy_score'),
            step_order=data.get('step_order')
        )
        return Response({"status": "Exercise logged"}, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post', 'put'], url_path='performance')
    def performance(self, request, pk=None):
        session = self.get_object()
        
        exercise_id = request.data.get('exercise_id')
        accuracy_score = request.data.get('accuracy_score')
        completed_reps = request.data.get('completed_reps')
        common_errors = request.data.get('common_errors', [])
        #feedback_summary = request.data.get('feedback_summary', '')
        step_order = request.data.get('step_order', 1) 

        if not exercise_id:
            return Response({"message": "exercise_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        session_exercise, created = SessionExercise.objects.update_or_create(
            session=session,
            exercise_id=exercise_id,
            defaults={
                'accuracy_score': accuracy_score,
                'completed_reps': completed_reps,
                'step_order': step_order,
                'common_errors': common_errors
                #'feedback_summary': feedback_summary
            }
        )
        
        return Response({
            "performance_id": session_exercise.id,
            "session_id": session.id,
            "exercise_id": exercise_id,
            "accuracy_score": accuracy_score,
            "completed_reps": completed_reps,
            "message": "Performance data submitted successfully."
        }, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='end')
    def end(self, request, pk=None):
        session = self.get_object()
        duration_minutes = request.data.get('duration_minutes')

        session.status = 'completed'
        session.ended_at = timezone.now()
        if duration_minutes is not None:
            session.duration_minutes = duration_minutes
        elif session.started_at:
            delta = session.ended_at - session.started_at
            session.duration_minutes = int(delta.total_seconds() / 60)
        session.save()
        
        #request'ten common_errors gibi veriler çekilebilir
        PerformanceAnalyzer.generate_and_save_summary(session, [])
        return Response({
            "session_id": session.id,
            "message": "Workout session marked as completed."
        }, status=status.HTTP_200_OK)
        session = self.get_object()
        performance_data = request.data.get('exercises', [])
        
        for exercise_data in performance_data:
            SessionExercise.objects.update_or_create(
                session=session,
                step_order=exercise_data.get('step_order'),
                defaults={
                    'exercise_id': exercise_data.get('exercise_id'),
                    'completed_reps': exercise_data.get('completed_reps'),
                    'completed_seconds': exercise_data.get('completed_seconds'),
                    'accuracy_score': exercise_data.get('accuracy_score')
                    #'errors': exercise_data.get('errors', []) ?
                }
            )
        
        session.status = 'completed'
        session.ended_at = timezone.now()
        if session.started_at:
            delta = session.ended_at - session.started_at
            session.duration_minutes = int(delta.total_seconds() / 60)
        session.save()
        PerformanceAnalyzer.generate_and_save_summary(session, session_common_errors)
        return Response({
            "status": "Performance data saved and summary generated.",
            "duration_minutes": session.duration_minutes
        }, status=status.HTTP_200_OK)

class SessionExerciseViewSet(viewsets.ModelViewSet):
    queryset = SessionExercise.objects.all()
    serializer_class = SessionExerciseSerializer

class SessionSummaryViewSet(viewsets.ModelViewSet):
    queryset = SessionSummary.objects.all()
    serializer_class = SessionSummarySerializer

class UserStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)

        stats_by_day = WorkoutSession.objects.filter(
            user=user,
            session_date__gte=seven_days_ago,
            status='completed'
        ).values('session_date').annotate(
            workout_count=Count('id'),
            avg_accuracy=Avg('overall_accuracy_score')
        ).order_by('session_date')

        total_summary = WorkoutSession.objects.filter(
            user=user, 
            status='completed'
        ).aggregate(
            total_workouts=Count('id'),
            total_avg_accuracy=Avg('overall_accuracy_score')
        )

        return Response({
            "daily_stats": stats_by_day,
            "overall": {
                "total_completed": total_summary['total_workouts'] or 0,
                "average_performance": round(total_summary['total_avg_accuracy'] or 0, 2),
                "streak_days": self._calculate_streak(user) # US-04 streak hesaplama
            }
        })

    def _calculate_streak(self, user):
        from django.utils.timezone import now
        from datetime import timedelta

        dates = WorkoutSession.objects.filter(
            user=user, status='completed'
        ).values_list('session_date', flat=True).distinct().order_by('-session_date')
        
        streak = 0
        current_date = now().date()
        
        for date in dates:
            if date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif date == current_date - timedelta(days=1):
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
                
        return streak