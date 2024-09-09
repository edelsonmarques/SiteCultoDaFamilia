from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
from enums import enums
from enums.env_deta import SECRET_KEY, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
import pymysql

load_dotenv()
pymysql.install_as_MySQLdb()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('LOCAL'):
    DEBUG = True
else:
    DEBUG = False
    

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    
    # jwt authentication
    'rest_framework',
    'rest_framework_simplejwt',
    
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.amazon',
    'allauth.socialaccount.providers.apple',
    'allauth.socialaccount.providers.exist',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.figma',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.okta',
    'allauth.socialaccount.providers.spotify',
    'allauth.socialaccount.providers.telegram',
    'allauth.socialaccount.providers.trello',
    
    
    # MyApps
    'cultoparafamilia',
    'cultoparafamilia.arearestritafamilia',
    'cultoparafamilia.sorteio_familia',
    'cultoparafamilia.sorteio_familia.configuracoes_sorteio',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # allauth
    "allauth.account.middleware.AccountMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = f'{enums.SITE_NAME}.urls'
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates', 'html')],
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

WSGI_APPLICATION = f'{enums.SITE_NAME}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agenda66',
        "USER": 'cultodafamilia',
        "PASSWORD": 'uFlZMckAfmvprDeXPlzyzXL3shQHaa4I',
        "HOST": 'dpg-crfcsotsvqrc73f73aa0-a',
        "PORT": 5432,
        'OPTIONS': {
            'autocommit': True,
            # 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'" ,
            # "use_pure": True
            }
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates', 'static'),)
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))
# STATIC_ROOT = './static'
STATIC_URL = 'static/'
# STATIC_ROOT = '/var/www/site/templates/static'
# STORAGES = {
# #     "default": {
# #         "BACKEND": "django.core.files.storage.FileSystemStorage",
# #     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
#     },
# }
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage' 

MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
