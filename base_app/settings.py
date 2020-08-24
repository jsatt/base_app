import logging
import os

import environ

BASE_DIR = (environ.Path(__file__) - 2)()
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

BASE_URL = env.str('BASE_URL', default='localhost')
TESTING = env.bool('TESTING', default=False)

#########
# DJANGO SETTINGS
#########
DEBUG = env.bool('DEBUG', default=False)

# SITE
WSGI_APPLICATION = 'base_app.wsgi.application'
ROOT_URLCONF = 'base_app.urls'
SECRET_KEY = env.str('SECRET_KEY', default='keepitsecret')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[BASE_URL])

# Databases
DATABASES = {
    'default': env.db('DATABASE_URL', default="sqlite://:memory:"),
}

CACHES = {
    'default': env.cache('CACHE_URL', default='dummycache://'),
}

# LOCALE
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# APPS
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'django_celery_beat',
    'django_extensions',
    'django_filters',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.celery',
    'rest_framework',
    'rest_framework.authtoken',

    # Local
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

# AUTH
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

# LOGGING
log_level = env.str('LOG_LEVEL', default='INFO')
log_formatter = env.str('LOG_FORMATTER', default='plain')
log_format = env.str('LOG_FORMAT', default=(
    '%(asctime)s %(levelname)s %(process)s %(thread)s [%(name)s] '
    '[%(pathname)s:%(lineno)d:%(funcName)s] - %(message)s'
))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'plain': {
            'format': log_format,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': log_formatter,
            'level': log_level,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': log_level,
    },
    'loggers': {
        'celery': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.request': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'gunicorn': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

#########
# REST FRAMEWORK
#########

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}


#########
# CELERY
#########

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'fanout_prefix': True,
    'fanout_patterns': True,
}
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='dummycache://')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='dummycache://')
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_ACKS_LATE = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_WORKER_PREFETCH_MULTIPLIER = 1


#########
# TESTS
#########
if TESTING:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
