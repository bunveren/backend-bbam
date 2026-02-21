from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserController, UserProfileViewSet, DeviceViewSet

router = DefaultRouter()
router.register(r'users', UserController, basename='users')
router.register(r'profiles', UserProfileViewSet, basename='profiles')
router.register(r'devices', DeviceViewSet, basename='devices')

urlpatterns = [
    path('', include(router.urls)),
]