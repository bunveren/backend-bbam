class NotificationService:
    @staticmethod
    def send_push_notification(user, title, message, extra_data=None):
        """
        TODO:
        Expo Push API entegrasyonu burada yapılacak.
        Kullanıcının veritabanındaki (UserDevice modelindeki) expo_token 
        bilgisi çekilerek ilgili cihaza bildirim atılacak.
        """
        pass

    @staticmethod
    def send_sync_signal(user):
        """
        TODO:
        Mobil cihaza silent push atacak fonksiyon.
        """
        pass