from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AppUser, UserProfile, UserDevice
from .serializers import AppUserSerializer, UserProfileSerializer, UserDeviceSerializer
from .services import UserManager, TokenService

class UserController(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    def create(self, request):
        user = UserManager.register_user(request.data['email'], request.data['password'])
        return Response({"user_id": user.id, "message": "user created successfully!!"}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        user = UserManager.validate_credentials(request.data['email'], request.data['password'])
        if user:
            token = TokenService.generate_jwt(user)
            return Response({"token": token, "user_id": user.id})
        return Response({"error": "Invalid credentials"}, status=401)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def list(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
   
class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = UserDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='unregister/(?P<uuid>[^/.]+)')
    def unregister(self, request, uuid=None):
        deleted_count, _ = UserDevice.objects.filter(user=request.user, device_uuid=uuid).delete()
        if deleted_count > 0:
            return Response({"message": "Device unregistered"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)