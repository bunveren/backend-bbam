from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutController, ExerciseLibraryViewSet

router = DefaultRouter()
router.register(r'plans', WorkoutController, basename='plans')
router.register(r'exercises', ExerciseLibraryViewSet, basename='exercises')
#router.register(r'reminders', NotificationController, basename='reminders')

urlpatterns = [path('', include(router.urls))]