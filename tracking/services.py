from django.db.models import Avg, F, Window
from django.db.models.functions import Lead
from .models import WorkoutSession, SessionSummary

class PerformanceDataProcessor:
    @staticmethod
    def process_incoming_session(data):
        return data #burada sessionu belki özet geçeriz

class PerformanceAnalyzer:
    @staticmethod
    def calculate_overall_score(session):
        exercises = session.sessionexercise_set.all()
        if not exercises: return 0
        return sum(e.accuracy_score for e in exercises) / len(exercises)
    
    @staticmethod
    def generate_and_save_summary(session):
        exercises = session.sessionexercise_set.all()
        
        summary_data = {
            "overall_avg_score": float(session.overall_accuracy_score),
            "total_completed_reps": sum(e.completed_reps or 0 for e in exercises),
            "details": [
                {"name": e.exercise.name, "score": float(e.accuracy_score)} for e in exercises
            ]
        }
        
        SessionSummary.objects.update_or_create(
            session=session,
            defaults={"summary_json": summary_data}
        )

class ProgressAnalyzer:
    @staticmethod
    def get_user_progress(user_id, period='week'):
        return WorkoutSession.objects.filter(
            user_id=user_id, 
            status='completed'
        ).values('session_date', 'overall_accuracy_score').order_by('session_date')

    @staticmethod
    def calculate_accuracy_delta(user_id):
        sessions = WorkoutSession.objects.filter(
            user_id=user_id, 
            status='completed'
        ).order_by('-session_date')[:2]
        
        if len(sessions) < 2:
            return 0
        
        return sessions[0].overall_accuracy_score - sessions[1].overall_accuracy_score