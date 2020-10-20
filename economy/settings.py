"""
Django settings for economy project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from kombu import serialization

import psycopg2.extensions
import ujson
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from django.urls import path, include, reverse, reverse_lazy

from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default_value')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['*']

INTERNAL_IPS = []

def custom_show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djmoney',
    'users',
    'sorl.thumbnail',
    'economy',
    'crispy_forms',
    'celery',
    'django_celery_beat',
    'debug_toolbar',
    'channels',
    'django_extensions',
    'flags',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'economy.middleware.URLChangeMiddleware',
]

ROOT_URLCONF = 'economy.urls'

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
            'libraries': {
                'cron_tags': 'templatetags.cron_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'economy.wsgi.application'
ASGI_APPLICATION = "economy.routing.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'economy_db',
        'USER': 'root',
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password123'),
        'HOST': 'database',
        'PORT': 5432,
    },
    'OPTIONS': {
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ["redis://redis:6379/6"],
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/2',
        'OPTIONS': {
            'CONNECTION_POOL_KWARGS': {'max_connections': 200},
            'CLIENT_CLASS': 'django_redis.client.default.DefaultClient'
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/web/media'
STATIC_ROOT = '/home/web/static'
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = reverse_lazy('login')


CELERY_BROKER_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//')
CELERY_TASK_IGNORE_RESULT = True
CELERY_TASK_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_TASK_SOFT_TIME_LIMIT = 24*60*60
# REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
# CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:6379'
CELERY_RESULT_COMPRESSION = 'gzip'


CELERY_ACCEPT_CONTENT = ['ujson']
CELERY_TASK_SERIALIZER = 'ujson'
CELERY_RESULT_SERIALIZER = 'ujson'

# uJSON is faster than json

serialization.register(
    'ujson',
    ujson.dumps,
    ujson.loads,
    content_type='application/x-ujson',
    content_encoding='utf-8'
)

# uJSON is faster than json

serialization.register(
    'ujson',
    ujson.dumps,
    ujson.loads,
    content_type='application/x-ujson',
    content_encoding='utf-8'
)

CELERY_TASK_ROUTES = {
    'economy.tasks.choose_winner': {'queue': 'tasks'},
}

CELERY_TASK_QUEUES = []

CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE', 'UTC')

# Celery beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
'lottery': {
'task': 'economy.tasks.choose_winner',
'schedule': crontab(hour='23'),
'args': (),
},
}


# These creds are used for pushing DNS records to AWS route53
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
DOMAIN = os.environ.get('DOMAIN', '')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'CSI_DB_Trial': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'daphne': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG'
        },

    }
}

FLAGS = {
    'PUSHING_SUBDOMAIN_TO_ROUTE53': [],
    'GIVING_DEFAULT_ITEMS_WHEN_PROFILE_CREATED': [],

}

sentry_sdk.init(
    dsn="http://f6476a79a8794852893d6105a15cc015@sentry.localhost/1",
    integrations=[DjangoIntegration()]
)

# Local settings for debugging and local info
try:
    from economy.local_settings import *
except ImportError:
    pass
