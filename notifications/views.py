from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import WorkoutReminder
from .serializers import WorkoutReminderSerializer
from .services import NotificationService

# Create your views here.
class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return WorkoutReminder.objects.all()
        return WorkoutReminder.objects.filter(user=user)
    
    def _trigger_sync(self, request):
        sender_device_uuid = request.headers.get('X-Device-UUID')
        if sender_device_uuid:
            print("sender uuid bulundu")
            NotificationService.send_silent_sync_signal(request.user, sender_device_uuid)
        else:
            print("DEBUG: Sinyal gönderilmedi çünkü X-Device-UUID header'ı eksik!")

    def perform_create(self, serializer):
        reminder = serializer.save(user=self.request.user)
        self._trigger_sync(self.request)

    def perform_update(self, serializer):
        serializer.save()
        self._trigger_sync(self.request)

    def perform_destroy(self, instance):
        instance.delete()
        self._trigger_sync(self.request)