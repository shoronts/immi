from pathlib import Path
from env import *


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'seerequirments'

DEBUG = EnvConfig.DEBUG
ALLOWED_HOSTS = EnvConfig.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Text Editor
    'ckeditor',
    'ckeditor_uploader',
    # My Apps
    'immi_theme',
    'immi_user',
    'immi_user_analysis',
    'immi_fourm',
    'immi_message',
]

CKEDITOR_UPLOAD_PATH = "inTextPicture/"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'immi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'immi.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = BASE_DIR, 'static'
# STATIC_ROOT = '/home/georvxgp/immi.squaretechit.com/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'
# MEDIA_ROOT = '/home/georvxgp/immi.squaretechit.com/media'

LOGIN_REDIRECT_URL = 'forum'
LOGIN_URL = 'login'


# CKEditor Configuration Settings
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar': 'full',
        'width': 'auto',
        'height': 'auto',
        }
    }


# EMAIL Configurations
EMAIL_HOST = EnvConfig.EMAIL_HOST
EMAIL_PORT = EnvConfig.EMAIL_PORT
EMAIL_HOST_USER = EnvConfig.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EnvConfig.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = EnvConfig.EMAIL_USE_TLS
EMAIL_USE_SSL = EnvConfig.EMAIL_USE_SSL

