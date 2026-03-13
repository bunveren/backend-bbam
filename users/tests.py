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

class UserRegisterAPITest(APITestCase):
    def setUp(self):
        self.url = "/api/users/register/"

    def test_succesfull_registration(self):
        payload = {
            "email": "newuser@test.com",
            "password": "strong_psswrd"
        }
        response = self.client.post(self.url, payload, format='json')
        #print("response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AppUser.objects.count(), 1)
        self.assertTrue(UserProfile.objects.filter(user__email="newuser@test.com").exists())

    def test_registration_duplicate_email(self):
        AppUser.objects.create(email="same_email@test.com", password_hash="strong_psswrd")
        payload = {
            "email": "same_email@test.com",
            "password": "different_password"
        }
        response = self.client.post(self.url, payload, format='json')
        #print("response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_fields(self):
        payload = {"email": "user@test.com"}
        response = self.client.post(self.url, payload, format='json')
        #print("response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginAPITest(APITestCase):
    def setUp(self):
        self.url = "/api/users/login/"
        self.user = UserManager.register_user("user_login@test.com", "strong_psswrd")

    def test_user_login(self):
        data = {"email": "user_login@test.com", "password": "strong_psswrd"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_wrong_password(self):
        data = {"email": "user_login@test.com", "password": "wrong_password"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_wrong_email(self):
        data = {"email": "Different_user@test.com", "password": "strong_psswrd"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_missing_field(self):
        data = {"email": "user_login@test.com"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_user_login_empty_values(self):
        data = {"email": "", "password": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_profile_update(self):  # PATCH	/api/users/profiles/{id}/
    #     user = UserManager.register_user("profileuser", "password")
    #     self.client.force_authenticate(user=user)
    #     url = reverse('profiles-detail', kwargs={'pk': user.id})
    #     data = {"user_name": "John" ,"height_cm": 180, "weight_kg": 75, "age": 25}
    #     response = self.client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['user_name'], "John")
    #     self.assertEqual(response.data['height_cm'], 180)
    #     self.assertEqual(response.data['weight_kg'], 75)
    #     self.assertEqual(response.data['age'], 25)    



class SecurityTest(APITestCase):
    def test_access_other_user_session(self):
        user1 = AppUser.objects.create(email="user1@test.com")
        user2 = AppUser.objects.create(email="user2@test.com")
        session_u1 = WorkoutSession.objects.create(user=user1, session_date="2026-01-01", started_at=timezone.now())
        
        self.client.force_authenticate(user=user2)
        url = f"/api/tracking/sessions/{session_u1.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)