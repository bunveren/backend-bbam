# Body and Beyond AI Mentor Backend
BBAM kullanıcıların antrenmanlarını takip etmelerini, yapay zeka destekli form analizi ve geri bildirim almalarını sağlayan bir fitness takip platformunun backend servisidir. Django ve Django REST Framework kullanılarak geliştirilmiştir.

## Özellikler
* **Kullanıcı Yönetimi:** JWT tabanlı kimlik doğrulama, profil yönetimi ve cihaz senkronizasyonu.
* **Antrenman Planlama:** Özelleştirilebilir egzersiz kütüphanesi ve antrenman planları.
* **Performans Takibi:** Antrenman oturumlarının gerçek zamanlı loglanması, accuracy skorları ve streak hesaplama.
* **Yapay Zeka Geri Bildirimleri:** Antrenman sonrasında performans verilerini analiz eden LLM entegrasyonu (umarım).
* **Hatırlatıcılar ve Bildirimler:** Özelleştirilebilir antrenman hatırlatıcıları ve Expo üzerinden push notification desteği.

## Tech Stack
- **Framework:** Django 5.2.x & Django REST Framework
- **Veritabanı:** PostgreSQL
- **Geliştirici Araçları:** Django Extensions (Graph models, Shell plus)
- **Kimlik Doğrulama:** Simple JWT (OAuth2 uyumlu)
- **Dokümantasyon:** drf-spectacular (Swagger UI / OpenAPI 3.0)
- **Test:** Model Bakery

## Başlangıç
Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:
 1. Depoyu clonelayın
 2. Sanal ortam oluşturun ve aktif edin
 3. Bağımlılıkları yükleyin: `pip install -r requirements.txt`
 4. Veritabanı ayarları: Yerel PostgreSQL veritabanınızda `bbam_db` adında bir veritabanı oluşturun. `core_project/settings.py` dosyasındaki `DATABASES` ayarlarını kendi yerel kullanıcı adınız ve şifrenizle güncelleyin.
### 5. Migrasyonları çalıştırın & sunucuyu başlatın
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## API Dokümantasyonu
Sunucu çalıştıktan sonra API uç noktalarını ve kullanım detaylarını Swagger üzerinden görebilirsiniz: `http://127.0.0.1:8000/api/docs/` 

## Testleri Çalıştırma
Projedeki testleri koşturmak için:
```
python manage.py test
```

## Katkıda Bulunma
1. Bu projeyi fork'layın.
2. Yeni bir feature branch oluşturun.
3. Değişikliklerinizi commit edin ve dala pushlayın.
4. Pull Request açın.
**Not:** Proje üzerinde çalışırken `X-Device-UUID` gibi özel header bilgilerinin bildirim servisleri için gerekli olduğunu unutmayın.
