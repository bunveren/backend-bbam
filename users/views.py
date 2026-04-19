from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AppUser, UserProfile, UserDevice
from .serializers import AppUserSerializer, TokenRefreshSerializer, UserProfileSerializer, UserDeviceSerializer
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
    
    @action(detail=False, methods=['post'], url_path='token/refresh', permission_classes=[])
    def refresh_token(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        refresh_token_string = serializer.validated_data.get('refresh')

        try:
            token = RefreshToken(refresh_token_string)
            user_id = token['user_id']
            
            user = AppUser.objects.filter(id=user_id).first()
            if not user:
                raise TokenError("User associated with this token no longer exists.")

            new_tokens = TokenService.generate_jwt(user)
            
            return Response({
                "access": new_tokens['access'],
                "refresh": new_tokens['refresh']
            }, status=status.HTTP_200_OK)

        except (TokenError, InvalidToken) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({"detail": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]   
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)

    # def get_object(self):
    #     profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
    #     return profile

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        return Response({"detail": "You do not have permission for this operation."}, status=status.HTTP_403_FORBIDDEN)
        # profile = self.get_object()
        # serializer = self.get_serializer(profile)
        # return Response(serializer.data)
   
class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = UserDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserDevice.objects.all()
        return UserDevice.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        device_uuid = request.data.get('device_uuid')
        expo_token = request.data.get('expo_token')
        os_type = request.data.get('os_type')

        if not device_uuid or not expo_token:
            return Response(
                {"error": "device_uuid and expo_token are mandatory."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        exists = UserDevice.objects.filter(user=request.user, device_uuid=device_uuid).exists()
        if not exists and UserDevice.objects.filter(user=request.user).count() >= 3:
            return Response({"error": "Device limit reached (Max 3)."}, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['delete'], url_path='unregister/(?P<uuid>[^/.]+)')
    def unregister(self, request, uuid=None):
        deleted_count, _ = self.get_queryset().filter(device_uuid=uuid).delete()
        if deleted_count > 0:
            return Response({"message": "Device unregistered"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
    
    #SİLMEYİN İLERDE KULLANILABİLİR
    def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)
        return Response({"detail": "Remote logout by ID is disabled for now. Use /unregister/{uuid}/"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)