from django.db import models

class AppUser(models.Model):
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'User'

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    height_cm = models.IntegerField(blank=True, null=True)
    weight_kg = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user_profiles'
        
class UserDevice(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='devices')
    device_uuid = models.CharField(max_length=255)
    expo_token = models.CharField(max_length=255)
    os_type = models.CharField(max_length=50, choices=[('ios', 'ios'), ('android', 'android')])
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_devices'
        unique_together = ('user', 'device_uuid')