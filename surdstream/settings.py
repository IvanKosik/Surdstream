"""
Django settings for surdstream project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'translations.apps.TranslationsConfig',
    'rest_framework',
    'widget_tweaks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'surdstream.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates', ],
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

WSGI_APPLICATION = 'surdstream.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='surdstream_db'),
        'USER': config('DB_USER', default='surdstream_db_admin'),
        'PASSWORD': config('DB_PASSWORD', default='admin'),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default=5432, cast=int),
    }
}
# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True


AUTH_USER_MODEL = 'translations.User'

# Redirect to home URL after login (default redirects to /accounts/profile/)
# LOGIN_REDIRECT_URL = '/'
# Redirect to this page, if user has to login to see another page
# LOGIN_URL = '/'
# LOGOUT_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'files', 'media')
MEDIA_URL = '/media/'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG \
    else 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('MAILGUN_SMTP_SERVER', default='smtp.mailgun.org')
EMAIL_PORT = config('MAILGUN_SMTP_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('MAILGUN_SMTP_LOGIN', default='')
EMAIL_HOST_PASSWORD = config('MAILGUN_SMTP_PASSWORD', default='')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@surd.stream'


LOG_TO_FILE = config('LOG_TO_FILE', default=False, cast=bool)
if LOG_TO_FILE:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'debug.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_URI = 'https://www.googleapis.com/upload/youtube/v3/videos'
YOUTUBE_UPLOAD_SCOPE = 'https://www.googleapis.com/auth/youtube.upload'
YOUTUBE_AUTH_CLIENT_ID = config('YOUTUBE_AUTH_CLIENT_ID')
YOUTUBE_AUTH_CLIENT_SECRET = config('YOUTUBE_AUTH_CLIENT_SECRET')
GOOGLE_AUTH_URI = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
# Need to add the redirect URI in the developer console
YOUTUBE_AUTH_WEB_REDIRECT_URI = 'http://www.surd.stream/youtube_auth_completed'
# Got refresh token using https://developers.google.com/oauthplayground
# (in settings setup client id and secret)
YOUTUBE_AUTH_REFRESH_TOKEN = config('YOUTUBE_AUTH_REFRESH_TOKEN')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/'files',
#%STATIC_ROOT = os.path.join(BASE_DIR, 'files', 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
