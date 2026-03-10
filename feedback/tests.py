from django.test import TestCase
from feedback.services import AIFeedbackEngine

class FeedbackServiceTests(TestCase):
    def test_ai_analysis_generation(self):
        sample_data = {
            "duration_minutes": 20,
            "avg_form_accuracy": 90,
            "common_errors": ["Düşük kalça"]
        }
        result = AIFeedbackEngine.generate_post_workout_analysis(sample_data)
        self.assertIn("20 dakikalık", result)
        self.assertIsInstance(result, str)
        self.assertIn("Düşük kalça", result)
        
    def test_ai_analysis_generation_bad(self):
        bad_session = {
            "avg_form_accuracy": 40,
            "common_errors": ["Sırt eğriliği", "Düşük kalça"],
            "duration_minutes": 10
        }
        feedback = AIFeedbackEngine.generate_post_workout_analysis(bad_session)
        self.assertIn("hatalar performansını düşürüyor", feedback)
        self.assertIn("Sırt eğriliği", feedback)