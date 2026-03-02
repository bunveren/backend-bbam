from rest_framework import serializers
from .models import AppUser, UserProfile, UserDevice

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['height_cm', 'weight_kg', 'age', 'gender', 'created_at']

class AppUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = AppUser
        fields = ['id','email', 'created_at']

class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['id', 'device_uuid', 'expo_token', 'os_type', 'last_active']
        read_only_fields = ['id', 'last_active']