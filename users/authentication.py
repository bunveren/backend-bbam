import jwt
from rest_framework import authentication, exceptions
from .models import AppUser

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
            user = AppUser.objects.get(id=payload['user_id'])
            return (user, token) 
        except (jwt.ExpiredSignatureError, jwt.DecodeError, AppUser.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid or expired token')

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