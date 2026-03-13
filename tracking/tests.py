from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker
from unittest.mock import patch
from django.contrib.auth import get_user_model
from users.models import AppUser
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

from users.models import AppUser
from workout.models import Exercise, WorkoutPlan
from tracking.models import WorkoutSession, SessionExercise, SessionSummary

User = get_user_model()

class TrackingModuleTests(APITestCase):
    def setUp(self):
        self.user = baker.make(AppUser)
        self.client.force_authenticate(user=self.user)
        self.plan = baker.make('workout.WorkoutPlan', user=self.user)
        self.session = baker.make('tracking.WorkoutSession', user=self.user, plan=self.plan, status='in_progress')
        self.exercise = baker.make(Exercise, name="Squat")

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
        
    def test_it_05_sync_offline_bundle(self):
        """[IT-05] Tamamlanmış offline antrenman paketinin senkronizasyonu (POST /api/tracking/sessions/sync/)"""
        url = '/api/tracking/sessions/sync/'
        
        sync_data = {
            "session_date": timezone.now().date().isoformat(),
            "started_at": (timezone.now() - timedelta(minutes=30)).isoformat(),
            "ended_at": timezone.now().isoformat(),
            "duration_minutes": 30,
            "overall_accuracy": 85.0,
            "exercises": [
                {
                    "exercise_id": self.exercise.id,
                    "completed_reps": 12,
                    "accuracy_score": 80.0,
                    "step_order": 1,
                    "common_errors": ["HIPS_SAGGING"]
                },
                {
                    "exercise_id": self.exercise.id,
                    "completed_reps": 15,
                    "accuracy_score": 90.0,
                    "step_order": 2,
                    "common_errors": []
                }
            ]
        }

        response = self.client.post(url, sync_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("server_session_id", response.data)

        session_id = response.data['server_session_id']
        
        session = WorkoutSession.objects.get(id=session_id)
        self.assertEqual(session.status, 'completed')
        self.assertEqual(float(session.overall_accuracy_score), 85.0)

        exercise_count = SessionExercise.objects.filter(session=session).count()
        self.assertEqual(exercise_count, 2)

        summary_exists = SessionSummary.objects.filter(session=session).exists()
        self.assertTrue(summary_exists, "Sync sonrası SessionSummary oluşturulmalı.")

    def test_ut_16_accuracy_score_boundary(self):
        session = WorkoutSession.objects.create(user=self.user, session_date=timezone.now().date(), started_at=timezone.now())
        with self.assertRaises(ValidationError):
            item = SessionExercise(session=session, exercise=self.exercise, accuracy_score=105.00, step_order=1)
            item.full_clean()
 
    def test_ut_21_average_accuracy_calculation(self):
        """[UT-21] Ortalama doğruluk puanı hesaplama mantığı testi"""
        session = WorkoutSession.objects.create(
            user=self.user, 
            session_date=timezone.now().date(), 
            started_at=timezone.now(),
            status='completed',
            overall_accuracy_score=90.0
        )

        url = reverse('user-stats')
        response = self.client.get(url)
        self.assertEqual(response.data['overall']['average_performance'], 90.0)

    def test_it_13_start_workout_session(self):
        """Antrenman oturumu başlatma (session_date zorunlu)"""
        plan = WorkoutPlan.objects.create(user=self.user, plan_name="Test Plan")
        data = {
            "session_date": timezone.now().date().isoformat(),
            "plan": plan.id,
            "started_at": timezone.now().isoformat()
        }
        url = '/api/tracking/sessions/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_it_15_end_workout_session(self):
        """Seans sonlandırma"""
        session = WorkoutSession.objects.create(
            user=self.user, 
            session_date=timezone.now().date(),
            started_at=timezone.now()
        )
        url = f'/api/tracking/sessions/{session.id}/end/'
        response = self.client.post(url, {"duration_minutes": 30, "exercises": []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_it_37_performance_data_add_update(self):
        """[IT-37] Performans verisi ekleme ve güncelleme"""
        session = WorkoutSession.objects.create(
            user=self.user, 
            session_date=timezone.now().date(), 
            started_at=timezone.now()
        )
        url = f'/api/tracking/sessions/{session.id}/performance/'
        
        perf_data = {
            "exercise_id": self.exercise.id,
            "accuracy_score": 85.5,
            "completed_reps": 12,
            "step_order": 1,
            "common_errors": ["KNEE_VALGUS"]
        }
        response = self.client.post(url, perf_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(SessionExercise.objects.get(session=session).accuracy_score), 85.5)

    def test_it_40_overall_accuracy_calculation_on_session_end(self):
        """[IT-40] Seans sonlandırıldığında overall_accuracy_score'un doğru hesaplanıp hesaplanmadığı"""
        session = WorkoutSession.objects.create(
            user=self.user, 
            session_date=timezone.now().date(),
            started_at=timezone.now()
        )
        
        url = f'/api/tracking/sessions/{session.id}/end/'
        data = {
            "duration_minutes": 45,
            "exercises": [
                {
                    "exercise_id": self.exercise.id,
                    "completed_reps": 10,
                    "accuracy_score": 80.0,
                    "step_order": 1,
                    "common_errors": ["HIPS_SAGGING"]
                },
                {
                    "exercise_id": self.exercise.id,
                    "completed_reps": 12,
                    "accuracy_score": 100.0,
                    "step_order": 2,
                    "common_errors": []
                }
            ]
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        session.refresh_from_db()
        self.assertEqual(session.status, 'completed')
        
        self.assertIsNotNone(
            session.overall_accuracy_score, 
            "overall_accuracy_score hesaplanmamış (PerformanceAnalyzer servisini kontrol et)"
        )
        
        calculated_score = round(float(session.overall_accuracy_score), 2)
        self.assertEqual(calculated_score, 90.0)

    def test_it_14_log_session_exercise(self):
        """[IT-14] Oturum içi egzersiz kaydı (POST /api/tracking/sessions/{id}/log_exercise/)"""
        session = WorkoutSession.objects.create(user=self.user, session_date=timezone.now().date(), started_at=timezone.now())
        url = f'/api/tracking/sessions/{session.id}/log_exercise/'
        data = {
            "exercise_id": self.exercise.id,
            "accuracy_score": 88.5,
            "completed_reps": 10,
            "step_order": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_it_35_36_session_management(self):
        """[IT-35/36] Geçmiş oturumları listeleme ve güncelleme/silme"""
        session = WorkoutSession.objects.create(user=self.user, session_date=timezone.now().date(), started_at=timezone.now())
        self.assertEqual(self.client.get('/api/tracking/sessions/').status_code, status.HTTP_200_OK) #35
        
        # 36
        update_url = f'/api/tracking/sessions/{session.id}/'
        response = self.client.put(update_url, {
            "status": "completed", 
            "session_date": session.session_date.isoformat(),
            "started_at": session.started_at.isoformat()
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.delete(update_url).status_code, status.HTTP_204_NO_CONTENT)
 
    def test_ut_98_data_anonymization(self):
        """[UT-98] Veri anonimleştirme kontrolü (PII içermeyen depolama)"""
        session = WorkoutSession.objects.create(user=self.user, session_date=timezone.now().date(), started_at=timezone.now())
        summary_data = {"avg_accuracy": 90, "total_reps": 50}
        
        url = '/api/feedback/'
        response = self.client.post(url, {"session_id": session.id, "metrics": summary_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        summary = SessionSummary.objects.get(session=session)
        self.assertNotIn("test@bbam.com", str(summary.summary_json))
        self.assertIn("avg_accuracy", summary.summary_json['raw_metrics'])       
    
    def test_it_16_get_stats_summary(self):
        """[IT-16] İstatistik özetini çekme (Dashboard verisi)"""
        url = reverse('user-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('daily_stats', response.data)
        self.assertIn('streak_days', response.data['overall'])