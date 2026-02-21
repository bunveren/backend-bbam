from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutSessionViewSet, SessionExerciseViewSet, UserStatsView

router = DefaultRouter()
router.register(r'sessions', WorkoutSessionViewSet, basename='sessions')
router.register(r'exercises', SessionExerciseViewSet, basename='session-exercises')

urlpatterns = [
    path('', include(router.urls)), 
    path('stats/', UserStatsView.as_view(), name='user-stats'),
]