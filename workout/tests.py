from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker
#from django.contrib.auth import get_user_model; User = get_user_model()
from users.models import AppUser


class WorkoutModuleTests(APITestCase):
    def setUp(self):
        self.user = baker.make(AppUser)
        self.client.force_authenticate(user=self.user)
        self.exercises = baker.make('workout.Exercise', _quantity=3)

    def test_list_exercises(self):
        url = '/api/workout/exercises/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_workout_plan(self):
        url = '/api/workout/plans/'
        data = {
            "plan_name": "Güçlenme Planı",
            "items": [
                {
                    "exercise_id": self.exercises[0].id,
                    "step_order": 1,
                    "target_reps": 12
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['plan_name'], "Güçlenme Planı")