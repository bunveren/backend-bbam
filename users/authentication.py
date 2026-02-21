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