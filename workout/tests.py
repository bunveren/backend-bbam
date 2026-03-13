from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker
#from django.contrib.auth import get_user_model; User = get_user_model()
from users.models import AppUser
from django.urls import reverse
from workout.models import WorkoutPlan, WorkoutPlanItem


class WorkoutModuleTests(APITestCase):
    def setUp(self):
        self.user = baker.make(AppUser)
        self.client.force_authenticate(user=self.user)
        self.exercise = baker.make('workout.Exercise', name="Squat")
        other_exercises = baker.make('workout.Exercise', _quantity=2)
        self.exercises = [self.exercise] + other_exercises

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

    def test_ut_17_step_order_sorting(self):
        """Workout PlanItem içinde step_order sıralama mantığının testi"""
        plan = WorkoutPlan.objects.create(user=self.user, plan_name="Sıralama Testi")
        WorkoutPlanItem.objects.create(plan=plan, exercise=self.exercise, step_order=2, set_label=3, target_reps=10)
        WorkoutPlanItem.objects.create(plan=plan, exercise=self.exercise, step_order=1, set_label=3, target_reps=10)
        
        items = WorkoutPlanItem.objects.filter(plan=plan).order_by('step_order')
        self.assertEqual(items[0].step_order, 1)
        self.assertEqual(items[1].step_order, 2)

    def test_it_12_workout_plan_creation(self):
        """Antrenman planı oluşturma POST /api/workout/plans/ """
        data = {
            "plan_name": "Sabah Rutini",
            "items": [{"exercise": self.exercise.id, "sets": 3, "reps": 12}]
        }
        response = self.client.post('/api/workout/plans/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_it_34_workout_plan_deletion(self):
        """Antrenman planını silme DELETE /api/workout/plans/{id}/"""
        plan = WorkoutPlan.objects.create(user=self.user, plan_name="Silinecek Plan")
        response = self.client.delete(f'/api/workout/plans/{plan.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #self.assertFalse(WorkoutPlan.objects.filter(id=plan.id).exists()) soft deletedeyiz

    def test_it_28_30_exercise_admin_operations(self):
        """[IT-28/30] Yeni egzersiz tanımlama ve kütüphaneden silme (Admin)"""
        url = reverse('exercises-list')
        data = {"name": "Squat", "gif_url": "http://gym.com/squat.gif"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        ex_id = response.data['id']
        del_url = reverse('exercises-detail', args=[ex_id])
        response = self.client.delete(del_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_it_11_exercise_list_and_detail(self):
        """[IT-11] Egzersizleri listeleme ve detay görme (GET /api/workout/exercises/)"""
        list_response = self.client.get('/api/workout/exercises/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        
        detail_url = f'/api/workout/exercises/{self.exercise.id}/'
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['name'], "Squat")

    def test_it_29_exercise_update(self):
        """[IT-29] Egzersiz verisini güncelleme (PUT /api/workout/exercises/{id}/)"""
        url = f'/api/workout/exercises/{self.exercise.id}/'
        data = {"name": "Updated Squat", "gif_url": "http://example.com/new_squat.gif"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.name, "Updated Squat")

    def test_it_31_32_33_workout_plan_management(self):
        """[IT-31/32/33] Plan listeleme, detay ve güncelleme"""
        plan = WorkoutPlan.objects.create(user=self.user, plan_name="Eski Plan")
        self.assertEqual(self.client.get('/api/workout/plans/').status_code, status.HTTP_200_OK) #31
        self.assertEqual(self.client.get(f'/api/workout/plans/{plan.id}/').status_code, status.HTTP_200_OK) #32
        response = self.client.patch(f'/api/workout/plans/{plan.id}/', {"plan_name": "Yeni Plan"})
        self.assertEqual(response.status_code, status.HTTP_200_OK) #33