from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from .models import AppUser

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)
        try:
            user_id = validated_token['user_id']
            user = AppUser.objects.get(id=user_id)
            return (user, validated_token)
        except AppUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        # auth_header = request.headers.get('Authorization')
        # if not auth_header or not auth_header.startswith('Bearer '):
        #     return None
        
        # token = auth_header.split(' ')[1]
        # try:
        #     payload = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
        #     user = AppUser.objects.get(id=payload['user_id'])
        #     return (user, token) 
        # except (jwt.ExpiredSignatureError, jwt.DecodeError, AppUser.DoesNotExist):
        #     raise exceptions.AuthenticationFailed('Invalid or expired token')

from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CustomJWTScheme(OpenApiAuthenticationExtension):
    target_class = CustomJWTAuthentication  # String değil, direkt yukarıdaki sınıfı atıyoruz
    name = 'BearerAuth'
    
    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'Token değerinizi girin (Başına Bearer yazmanıza gerek yok).'
        }