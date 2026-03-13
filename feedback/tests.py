from django.test import TestCase
from feedback.services import AIFeedbackEngine
from users.models import AppUser
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from model_bakery import baker

class FeedbackServiceTests(APITestCase):
    def setUp(self):
        self.user = baker.make(AppUser)
        self.client.force_authenticate(user=self.user)
    
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
    
    def test_it_18_get_ai_feedback(self):
        """[IT-18] AI geri bildirimini alma (GET /api/feedback/)"""
        url = reverse('ai-feedback')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_it_41_background_feedback_generation(self):
        """[IT-41] Yeni geri bildirim oluşturma (Arka Plan) POST"""
        session = baker.make('tracking.WorkoutSession', user=self.user, status="completed")
        url = '/api/feedback/' 
        data = {"session_id": session.id}
        
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])