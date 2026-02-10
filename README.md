# backend-posest

db kurulumu: postgresql içerisinde default servera giriş yapın ve içine bbam_db adında database oluşturun. sırayla bbam_database.sql ve mock_data.sql i query sekmesinden open file ile açıp f5 ile çalıştırın. db bilgilerini settings.py'a girdiğinizden emin olun.

python manage.py inspectdb > models.py yapılmış halini commitledim, db değişikliğinde generate edilmeli ve models.py'lar değiştirilmelidir.
python manage.py migrate --fake-initial yaptım ki olanı güncellesin eskiye ekleme yapmaya çalışmasın

genel build alımı VENV ICINDE:
python manage.py makemigrations  
python manage.py migrate
opsiyonel: python manage.py shell  ile dbnin baglandıgı kontrol edilebilir
python manage.py createsuperuser ile admin üyeliği oluşturulur
python manage.py runserver
http://127.0.0.1:8000/admin e gidilip superuser bilgileri girilir ve dbnin geldiği kontrol edilebilir

settings.py içindeki db syntaxı:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

todo: model isimlendirmelerini değiştireceğim
