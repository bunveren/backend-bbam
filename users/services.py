from django.contrib.auth.hashers import make_password, check_password
from .models import AppUser, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager:
    @staticmethod
    def register_user(email, password):
        hashed_pw = make_password(password)
        user = AppUser.objects.create(email=email, password_hash=hashed_pw)
        UserProfile.objects.create(user=user)
        return user

    @staticmethod
    def validate_credentials(email, password):
        user = AppUser.objects.filter(email=email).first()
        if user and check_password(password, user.password_hash):
            return user
        return None

class TokenService:
    @staticmethod
    def generate_jwt(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),          
            'access': str(refresh.access_token), 
        }
        #payload = {'user_id': user.id, 'email': user.email}
        #return jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')