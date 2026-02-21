from .models import Exercise, ExerciseRule
from .serializers import ExerciseSerializer

class ExerciseLibraryService:
    @staticmethod
    def get_all_exercises():
        exercises = Exercise.objects.all()
        return ExerciseSerializer(exercises, many=True).data

    @staticmethod
    def get_rules_for_exercise(exercise_id):
        try:
            rule = ExerciseRule.objects.get(exercise_id=exercise_id, is_active=True)
            return rule.rules_json
        except ExerciseRule.DoesNotExist:
            return None