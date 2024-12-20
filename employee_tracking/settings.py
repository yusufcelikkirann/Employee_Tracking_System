
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8btou@hq&afpgk!(sd3_le0)a8rrq$!gy)l_m(slshxszhc+p+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'employee',
    'channels',
    'notifications',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF Middleware etkin olmalı
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'employee.middleware.NoCacheMiddleware',
]

ROOT_URLCONF = 'employee_tracking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'employee_tracking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'employee_tracking',
        'USER': 'postgres',
        'PASSWORD': 'admin_123',  
        'HOST': 'db',   # localde calistirmak icin 'localhost' yazilmali , eger docker kullanilacaksa db yazilmali. bu sekılde bash  ile çalıştırılıdıgnda utf-8 hatası veriyor 
        'PORT': '5432',
    }
}



REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_yasg.inspectors.AutoSchema',  # Bu satır eklendi
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'employee.CustomUser'




# settings.py
CELERY_BROKER_URL = 'redis://redis-container:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis-container:6379/0'

# Channels'ı ASGI sunucusu olarak ayarlama
ASGI_APPLICATION = 'employee_tracking.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Redis ile bağlantıyı sağlıyoruz
        },
    },
}

# settings.py

TIME_ZONE = 'Europe/Istanbul'
USE_TZ = True  # True olmalı, çünkü Django UTC ile çalışır.





JAZZMIN_SETTINGS = {
    "site_title": "My Admin Panel",
    "site_header": "Employee Tracker",
    "welcome_sign": "Welcome to the Employee Tracker Admin",
    "site_logo": "2ntech.jpeg",  # Logo dosyasının yolu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["auth"],
    "hide_models": ["auth.User"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",
    },
    "custom_css": None,
    "custom_js": None,
    "topmenu_links": [  # Navbar bağlantıları
        {
            "name": "Yonetici Paneli",  # Gözükecek isim
            "url": "admin_dashboard",  # Django URL adını kullanabilirsiniz
            "permissions": ["auth.view_user"],  # Bu linki görmek için gereken izinler (isteğe bağlı)
            "new_window": False,  # Yeni sekmede açmak istemiyorsanız
            "icon": "fas fa-tachometer-alt",  # Bir simge eklemek için
        },
    ],
}
