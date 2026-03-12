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
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {"error": "Email and password are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if AppUser.objects.filter(email=email).exists():
            return Response(
                {"error": "A user with this email already exists."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = UserManager.register_user(email, password) 
        return Response({"user_id": user.id, "message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password cannot be empty."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = UserManager.validate_credentials(email, password)  
        if user:
            tokens = TokenService.generate_jwt(user) 
            return Response({
                "access": tokens['access'],
                "refresh": tokens['refresh'],
                "user_id": user.id
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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

    def create(self, request, *args, **kwargs):
        device_uuid = request.data.get('device_uuid')
        expo_token = request.data.get('expo_token')
        os_type = request.data.get('os_type')

        if not device_uuid or not expo_token:
            return Response(
                {"error": "device_uuid and expo_token are mandatory."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        device, created = UserDevice.objects.update_or_create(
            user=request.user,
            device_uuid=device_uuid,
            defaults={
                'expo_token': expo_token,
                'os_type': os_type,
            }
        )

        serializer = self.get_serializer(device)
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='unregister/(?P<uuid>[^/.]+)')
    def unregister(self, request, uuid=None):
        deleted_count, _ = UserDevice.objects.filter(user=request.user, device_uuid=uuid).delete()
        if deleted_count > 0:
            return Response({"message": "Device unregistered"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)