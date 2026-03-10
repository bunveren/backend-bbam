from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutPlanViewSet, ExerciseLibraryViewSet

router = DefaultRouter()
router.register(r'plans', WorkoutPlanViewSet, basename='plans')
router.register(r'exercises', ExerciseLibraryViewSet, basename='exercises')

urlpatterns = [path('', include(router.urls))]