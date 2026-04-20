import os
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import pytz
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import WorkoutReminder
from .serializers import WorkoutReminderSerializer
from .services import NotificationService
from users.models import UserDevice

# Create your views here.
def trigger_reminders_view(request):
    expected_key = os.environ.get('CRON_SECRET_KEY')
    provided_key = request.headers.get('X-Cron-Key')
    if provided_key != expected_key:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    istanbul_tz = pytz.timezone('Europe/Istanbul')
    now_istanbul = timezone.now().astimezone(istanbul_tz)
    
    h = now_istanbul.hour
    m = now_istanbul.minute

    reminders = WorkoutReminder.objects.filter(
        reminder_time__hour=h,
        reminder_time__minute=m,
        is_active=True
    )

    count = 0
    for r in reminders:
        devices = UserDevice.objects.filter(user=r.user)
        tokens = [d.expo_token for d in devices if d.expo_token]

        if tokens:
            NotificationService.send_visible_push(
                tokens=tokens,
                title="Time for your workout session!",
                message=r.message or "Do something your future self will thank you for. Let's get moving! ",
                plan_id=r.plan.id if r.plan else None
            )
            count += 1

    return JsonResponse({
        "status": "completed",
        "server_time_istanbul": f"{h}:{m}",
        "reminders_found": reminders.count(),
        "notifications_sent_to_users": count
    })

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
            NotificationService.send_silent_sync_signal(request.user, sender_device_uuid)
        else:
            print("Error: sync function call failed")

    def perform_create(self, serializer):
        reminder = serializer.save(user=self.request.user)
        self._trigger_sync(self.request)

    def perform_update(self, serializer):
        serializer.save()
        self._trigger_sync(self.request)

    def perform_destroy(self, instance):
        instance.delete()
        self._trigger_sync(self.request)