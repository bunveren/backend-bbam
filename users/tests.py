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
            "email": "newuser@gmail.com",
            "password": "strong_psswrd"
        }
        response = self.client.post(self.url, payload, format='json')
        #print("response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AppUser.objects.count(), 1)
        self.assertTrue(UserProfile.objects.filter(user__email="newuser@gmail.com").exists())

    def test_registration_duplicate_email(self):
        AppUser.objects.create(email="same_email@gmail.com", password_hash="strong_psswrd")
        payload = {
            "email": "same_email@gmail.com",
            "password": "different_password"
        }
        response = self.client.post(self.url, payload, format='json')
        #print("response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_fields(self):
        payload = {"email": "user@gmail.com"}
        response = self.client.post(self.url, payload, format='json')
        #print("response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginAPITest(APITestCase):
    def setUp(self):
        self.url = "/api/users/login/"
        self.user = UserManager.register_user("user_login@gmail.com", "strong_psswrd")

    def test_user_login(self):
        data = {"email": "user_login@gmail.com", "password": "strong_psswrd"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_wrong_password(self):
        data = {"email": "user_login@gmail.com", "password": "wrong_password"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_wrong_email(self):
        data = {"email": "Different_user@gmail.com", "password": "strong_psswrd"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_missing_field(self):
        data = {"email": "user_login@gmail.com"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_user_login_empty_values(self):
        data = {"email": "", "password": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)   

class UsersProfilesAPITest(APITestCase):
    def setUp(self):
        self.url = "/api/users/profiles/"
        self.user1 = UserManager.register_user("user1@gmail.com", "password1")
        self.user2 = UserManager.register_user("user2@gmail.com", "password2")
        self.user3 = UserManager.register_user("user3@gmail.com", "password3")
        
        profile_1 = self.user1.userprofile
        profile_1.user_name = "John"
        profile_1.height_cm = 180
        profile_1.weight_kg = 75
        profile_1.age = 25
        profile_1.save()
        
        profile_2 = self.user2.userprofile
        profile_2.user_name = "Alex"
        profile_2.height_cm = 170
        profile_2.weight_kg = 65
        profile_2.age = 22
        profile_2.save()
        
        profile_3 = self.user3.userprofile
        profile_3.user_name = "Matt"
        profile_3.height_cm = 187
        profile_3.weight_kg = 83
        profile_3.age = 28
        profile_3.save()
        
        self.admin_user = AppUser.objects.create(email="admin@gmail.com", is_staff=True)
        UserProfile.objects.create(user=self.admin_user, user_name="Admin")

    def test_get_all_profiles_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_all_profiles_regular_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class SingleUserProfileAPITest(APITestCase):
    def setUp(self):
        self.user1 = UserManager.register_user("user1@test.com", "pass123")
        self.user2 = UserManager.register_user("user2@test.com", "pass123")
        self.admin = AppUser.objects.create(email="admin@test.com", is_staff=True)

        profile_1 = self.user1.userprofile
        profile_1.user_name = "John"
        profile_1.height_cm = 180
        profile_1.weight_kg = 75
        profile_1.age = 25
        profile_1.save()
        
        profile_2 = self.user2.userprofile
        profile_2.user_name = "Alex"
        profile_2.height_cm = 170
        profile_2.weight_kg = 65
        profile_2.age = 22
        profile_2.save()
        
        self.url_1 = f"/api/users/profiles/{self.user1.id}/"
        self.url_2 = f"/api/users/profiles/{self.user2.id}/"

    def test_get_own_profile(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url_1)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_other_user_denied(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url_2)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_own_profile(self):
        self.client.force_authenticate(user=self.user1)
        payload = {"user_name": "Bella"}
        response = self.client.patch(self.url_1, payload)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_name'], "Bella")

    def test_put_own_profile(self):
        self.client.force_authenticate(user=self.user2)
        payload = {'user_name': 'Rick', 'height_cm': 174, 'weight_kg': 78, 'age': 20, 'gender': 'male'}
        response= self.client.put(self.url_2,payload)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_name'], "Rick")
        self.assertEqual(response.data['height_cm'], 174)
        self.assertEqual(response.data['weight_kg'], 78)
        self.assertEqual(response.data['age'], 20)   
        self.assertEqual(response.data['gender'], 'male') 

    def test_admin_can_access_any_profile(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url_1)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_own_profile(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.url_1)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_other_user_denied(self):
        self.client.force_authenticate(user=self.user1)
        payload = {"user_name": "Bella"}
        response = self.client.patch(self.url_2,payload)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_other_user_denied(self):
        self.client.force_authenticate(user=self.user1)
        payload = {"user_name": "Bella" , 'height_cm': 174, 'weight_kg': 78, 'age': 20, 'gender': 'female'}
        response = self.client.put(self.url_2,payload)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_other_user_denied(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.url_2)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_update_any_profile(self):
        self.client.force_authenticate(user=self.admin)
        payload = {"user_name": "Bella" , 'height_cm': 174,'gender': 'female'}
        response = self.client.patch(self.url_1,payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_name'], "Bella")
        self.assertEqual(response.data['height_cm'], 174)  
        self.assertEqual(response.data['gender'], 'female')

    def test_admin_can_delete_any_profile(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.url_1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# class UserDevicesAPITest (APITestCase):

# class SecurityTest(APITestCase):
#     def test_access_other_user_session(self):
#         user1 = AppUser.objects.create(email="user1@gmail.com")
#         user2 = AppUser.objects.create(email="user2@gmail.com")
#         session_u1 = WorkoutSession.objects.create(user=user1, session_date="2026-01-01", started_at=timezone.now())
        
#         self.client.force_authenticate(user=user2)
#         url = f"/api/tracking/sessions/{session_u1.id}/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)