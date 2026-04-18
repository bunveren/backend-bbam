from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import AppUser
from .models import WorkoutReminder
from workout.models import WorkoutPlan 
from users.models import UserDevice
from .services import NotificationService
from .serializers import WorkoutReminderSerializer
from unittest.mock import patch

class ReminderAPITests(APITestCase):
    def setUp(self):
        self.user1 = AppUser.objects.create(email="user1@gmail.com", password_hash="hash")
        self.user2 = AppUser.objects.create(email="user2@gmail.com", password_hash="hash")
        self.admin = AppUser.objects.create(email="admin@gmail.com", password_hash="hash", is_staff=True)

        self.reminder_user1 = WorkoutReminder.objects.create(
            user=self.user1, 
            reminder_time="08:00:00", 
            message="User 1 Reminder"
        )
        self.reminder_user2 = WorkoutReminder.objects.create(
            user=self.user2, 
            reminder_time="09:00:00", 
            message="User 2 Reminder"
        )

        self.plan_user1 = WorkoutPlan.objects.create(
        user=self.user1,
        plan_name="User 1's Private Plan"
        )
    
        self.plan_user2 = WorkoutPlan.objects.create(
            user=self.user2,
            plan_name="User 2's Private Plan"
        )

        self.list_url = reverse('workout-reminders-list')


    def test_regular_user_only_sees_own_reminders(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], "User 1 Reminder")

    def test_admin_sees_all_reminders(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


    def test_create_reminder_for_other_user_denied(self):
        self.client.force_authenticate(user=self.user2) 
        payload = {
            "reminder_time": "10:00:00",
            "message": "Invalid Reminder",
            "user": self.user1.id  
        }
        response = self.client.post(self.list_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user", response.data)
        self.assertFalse(WorkoutReminder.objects.filter(message="Invalid Reminder").exists())

    def test_invalid_recurrence_days_format(self):
        self.client.force_authenticate(user=self.user1)
        payload = {
            "reminder_time": "10:00:00",
            "recurrence_days": "Monday" 
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reminder_with_valid_days_array(self):
        self.client.force_authenticate(user=self.user1)
        days = [1, 3, 5] 
        
        payload = {
            "reminder_time": "08:30:00",
            "recurrence": "weekly",
            "recurrence_days": days,
            "message": "Morning Workout"
        }
        response = self.client.post(self.list_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reminder = WorkoutReminder.objects.get(message="Morning Workout")
        self.assertEqual(reminder.recurrence_days, days)
        self.assertIsInstance(reminder.recurrence_days, list)


    def test_access_other_user_reminder_id_denied(self):
        self.client.force_authenticate(user=self.user1)
        detail_url = reverse('workout-reminders-detail', args=[self.reminder_user2.id])
        
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_other_user_reminder_denied(self):
        self.client.force_authenticate(user=self.user1)
        detail_url = reverse('workout-reminders-detail', args=[self.reminder_user2.id])
        
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(WorkoutReminder.objects.filter(id=self.reminder_user2.id).exists())

    def test_get_own_reminder_detail(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('workout-reminders-detail', args=[self.reminder_user1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.reminder_user1.id)
        self.assertEqual(response.data['message'], "User 1 Reminder")

    def test_put_own_reminder_full_update(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('workout-reminders-detail', args=[self.reminder_user1.id])
        
        payload = {
            "reminder_time": "15:30:00",
            "recurrence": "daily",
            "message": "New message",
            "is_active": False
        }
        response = self.client.put(url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reminder_user1.refresh_from_db()
        self.assertEqual(self.reminder_user1.message, "New message")
        self.assertFalse(self.reminder_user1.is_active)

    def test_patch_own_reminder_partial_update(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('workout-reminders-detail', args=[self.reminder_user1.id])
        
        payload = {"is_active": False}
        response = self.client.patch(url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reminder_user1.refresh_from_db()
        self.assertFalse(self.reminder_user1.is_active)
        self.assertEqual(self.reminder_user1.message, "User 1 Reminder")

    def test_delete_own_reminder(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('workout-reminders-detail', args=[self.reminder_user1.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkoutReminder.objects.filter(id=self.reminder_user1.id).exists())

    def test_link_reminder_to_someone_elses_plan_denied(self):
        self.client.force_authenticate(user=self.user1)
        payload = {
            "reminder_time": "12:00:00",
            "plan": self.plan_user2.id,
            "message": "Attempting to link other's plan"
        }
        response = self.client.post(self.list_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("plan", response.data)
        self.assertFalse(WorkoutReminder.objects.filter(message="Attempting to link other's plan").exists())

    def test_link_reminder_to_deleted_plan_denied(self):
        self.client.force_authenticate(user=self.user1)
        self.plan_user1.delete() 
        payload = {
            "reminder_time": "14:00:00",
            "plan": self.plan_user1.id, 
            "message": "Linking to deleted plan"
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("plan", response.data)

class NotificationServiceUnitTests(APITestCase):
    def setUp(self):
        self.user = AppUser.objects.create(email="sync_user@gmail.com", password_hash="hash")
        
        self.device_a = UserDevice.objects.create(
            user=self.user, device_uuid="uuid-aaa", expo_token="token-aaa", os_type="ios"
        )
        self.device_b = UserDevice.objects.create(
            user=self.user, device_uuid="uuid-bbb", expo_token="token-bbb", os_type="android"
        )
        self.device_c = UserDevice.objects.create(
            user=self.user, device_uuid="uuid-ccc", expo_token="token-ccc", os_type="ios"
        )

    @patch('notifications.services.requests.post')
    def test_ut_23_filter_sender_device(self, mock_post):
        mock_post.return_value.status_code = 200
        NotificationService.send_silent_sync_signal(self.user, "uuid-aaa")
        
        self.assertTrue(mock_post.called)
        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        self.assertIn("token-bbb", payload['to'])
        self.assertIn("token-ccc", payload['to'])
        self.assertNotIn("token-aaa", payload['to'])
        self.assertEqual(payload['data']['type'], "REMINDER_SYNC")
        self.assertTrue(payload['contentAvailable'])

class ReminderValidationUnitTests(TestCase):
    def test_recurrence_days_must_be_array(self):
        bad_data = {
            "reminder_time": "08:00:00",
            "recurrence": "weekly",
            "recurrence_days": "Monday"
        }
        
        serializer = WorkoutReminderSerializer(data=bad_data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('recurrence_days', serializer.errors)

    def test_invalid_time_format_validation(self):
        bad_data = {
            "reminder_time": "99:99", #Geçersiz saat
            "recurrence": "once"
        }
        
        serializer = WorkoutReminderSerializer(data=bad_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reminder_time', serializer.errors)
