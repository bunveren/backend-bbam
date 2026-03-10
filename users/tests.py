from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import AppUser, UserProfile
from .services import UserManager
from tracking.models import WorkoutSession
from django.utils import timezone
from django.urls import reverse

class UserManagerTest(TestCase):
    def test_register_user_creates_profile(self):
        email = "test@example.com"
        password = "password123"
        user = UserManager.register_user(email, password)
        
        self.assertEqual(user.email, email)
        self.assertTrue(check_password(password, user.password_hash))
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

class UserAPITest(APITestCase):
    def test_user_login(self):
        user = UserManager.register_user("login@test.com", "securepass")
        url = "/api/users/login/"
        data = {"email": "login@test.com", "password": "securepass"}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_profile_update(self):
        user = UserManager.register_user("profileuser", "password")
        self.client.force_authenticate(user=user)
        url = reverse('profiles-detail', kwargs={'pk': user.id})
        data = {"height": 180, "weight": 75, "age": 25}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class SecurityTest(APITestCase):
    def test_access_other_user_session(self):
        user1 = AppUser.objects.create(email="user1@test.com")
        user2 = AppUser.objects.create(email="user2@test.com")
        session_u1 = WorkoutSession.objects.create(user=user1, session_date="2026-01-01", started_at=timezone.now())
        
        self.client.force_authenticate(user=user2)
        url = f"/api/tracking/sessions/{session_u1.id}/"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)