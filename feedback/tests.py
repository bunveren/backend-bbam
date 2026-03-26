from django.test import TestCase
from feedback.services import AIFeedbackEngine

class AIFeedbackEngineLiveTests(TestCase):
    def test_live_ai_analysis_good_performance(self):
        sample_data = {
            "duration_minutes": 45,
            "avg_form_accuracy": 88.5,
            "common_errors": ["HIPS_SAGGING"]
        }
        result = AIFeedbackEngine.generate_post_workout_analysis(sample_data)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 50)
        self.assertTrue(any(word in result.lower() for word in ["workout", "form", "accuracy", "hips", "performance"])        )

    def test_live_ai_analysis_poor_performance(self):
        bad_data = {
            "duration_minutes": 15,
            "avg_form_accuracy": 45.0,
            "common_errors": ["ROUNDED_BACK", "NECK_PULLED", "FAST_REP"]
        }
        result = AIFeedbackEngine.generate_post_workout_analysis(bad_data)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 50)
        
        lower_result = result.lower()
        self.assertTrue("rounded_back" in lower_result or "neck_pulled" in lower_result or "back" in lower_result)

    def test_live_ai_analysis_perfect_form(self):
        perfect_data = {
            "duration_minutes": 30,
            "avg_form_accuracy": 99.0,
            "common_errors": []
        }
        result = AIFeedbackEngine.generate_post_workout_analysis(perfect_data)
        
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 50)
        self.assertTrue(any(word in result.lower() for word in ["excellent", "great", "perfect", "no major form errors", "good job"]))