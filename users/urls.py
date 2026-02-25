from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserController, UserProfileViewSet, DeviceViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profiles')
router.register(r'devices', DeviceViewSet, basename='devices')

urlpatterns = [
    path('register/', UserController.as_view({'post': 'create'}), name='user-register'),
    path('login/', UserController.as_view({'post': 'login'}), name='user-login'),
    path('', include(router.urls)),
]