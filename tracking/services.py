from .models import WorkoutSession, SessionSummary
from feedback.services import AIFeedbackEngine

class PerformanceDataProcessor:
    @staticmethod
    def process_incoming_session(data):
        processed_data = {
            "session_id": data.get("session_id"),
            "exercises": len(data.get("exercises", [])),
            "timestamp": data.get("ended_at"),
            "is_valid": True if data.get("exercises") else False
        }
        return processed_data

class PerformanceAnalyzer:
    @staticmethod
    def calculate_overall_score(session):
        exercises = session.sessionexercise_set.all()
        if not exercises: return 0
        return sum(e.accuracy_score for e in exercises) / len(exercises)
    
    @staticmethod
    def generate_and_save_summary(session, common_errors):
        if common_errors is None:
            common_errors = []
        exercises = session.sessionexercise_set.all()
        total_accuracy = sum(ex.accuracy_score for ex in exercises if ex.accuracy_score)
        avg_accuracy = float(total_accuracy / exercises.count()) if exercises.exists() else 0

        summary_data = {
            "session_id": str(session.id),
            "duration_minutes": session.duration_minutes,
            "avg_form_accuracy": avg_accuracy,
            "common_errors": common_errors
        }
        
        ai_comment = AIFeedbackEngine.generate_post_workout_analysis(summary_data)
        summary_data["ai_summary"] = ai_comment
        
        SessionSummary.objects.update_or_create(
            session=session,
            defaults={"summary_json": summary_data}
        )
        session.overall_accuracy_score = avg_accuracy
        session.save(update_fields=['overall_accuracy_score'])

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