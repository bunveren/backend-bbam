from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker
from unittest.mock import patch
from django.contrib.auth import get_user_model
from users.models import AppUser

User = get_user_model()

class TrackingModuleTests(APITestCase):
    def setUp(self):
        self.user = baker.make(AppUser)
        self.client.force_authenticate(user=self.user)
        self.plan = baker.make('workout.WorkoutPlan', user=self.user)
        self.session = baker.make('tracking.WorkoutSession', user=self.user, plan=self.plan, status='in_progress')

    def test_log_exercise_performance(self):
        url = f'/api/tracking/sessions/{self.session.id}/log_exercise/'
        test_exercise = baker.make('workout.Exercise')
        data = {
            "exercise_id": test_exercise.id, 
            "accuracy_score": "85.50",
            "completed_reps": 10,
            "step_order": 1
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('tracking.views.PerformanceAnalyzer.generate_and_save_summary')
    def test_end_session_with_ai_mock(self, mock_ai_summary):
        mock_ai_summary.return_value = "Harika iş çıkardın, formun çok iyi!"
        url = f'/api/tracking/sessions/{self.session.id}/end/'
        data = {"duration_minutes": 30}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_ai_summary.called)
        self.assertEqual(response.data['status'], 'completed')

    def test_get_user_stats(self):
        baker.make('tracking.WorkoutSession', user=self.user, status='completed', _quantity=5)
        url = '/api/tracking/stats/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)