import requests
from django.conf import settings
import logging
from users.models import UserDevice 

logger = logging.getLogger(__name__)
class NotificationService:
    @staticmethod
    def send_silent_sync_signal(user, sender_device_uuid):
        devices = UserDevice.objects.filter(user=user).exclude(device_uuid=sender_device_uuid)
        
        if not devices.exists():
            return

        tokens = [d.expo_token for d in devices]

        payload = {
            "to": tokens,
            "data": {
                "type": "REMINDER_SYNC",
                "action": "REFRESH_REMINDERS"
            },
            "priority": "high",
            "contentAvailable": True
        }
        try:
            url = "https://exp.host/--/api/v2/push/send"
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Sync signal was successfully send to {len(tokens)} devices.")
            else:
                logger.error(f"Expo API Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection Error: {str(e)}")

    @staticmethod
    def send_visible_push(tokens, title, message, plan_id=None):
        payload = {
            "to": tokens, # Cihazların adresleri (liste)
            "title": title,
            "body": message,
            "sound": "default", 
            "priority": "high", 
            "data": {"plan_id": plan_id} 
        }
        try:
            r = requests.post("https://exp.host/--/api/v2/push/send", json=payload, timeout=10)
            print(f"Push Response: {r.text}") 
        except Exception as e:
            print(f"Push Error: {e}")