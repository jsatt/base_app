import logging
import os

import environ
import structlog
from ddtrace import tracer as dd_tracer

from utils.environment import Env

BASE_DIR = (environ.Path(__file__) - 2)()
env = environ.Env(os.path.join(BASE_DIR, '.env'))

BASE_URL = env.str('BASE_URL', default='localhost')
TESTING = env.bool('TESTING', default=False)
USE_DATADOG = env.bool('USE_DATADOG', default=False)
USE_SENTRY = env.bool('USE_SENTRY', default=False)

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
    'default': env.db_opts('DATABASE_URL', default="sqlite://:memory:", options={
        'CONN_MAX_AGE': env.int('DATABASE_CONNECTION_AGE', default=600),
    }),
}

CACHES = {
    'default': env.cache_opts('CACHE_URL', default='dummycache://', options={
        'OPTIONS': {'SERIALIZER': 'django_redis.serializers.json.JSONSerializer'},
    }),
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
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': log_format,
        },
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

structlog.configure(
    processors=[
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

#########
# SENTRY
#########
if USE_SENTRY:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    logging_integration = LoggingIntegration(
        level=getattr(logging, env.str('SENTRY_LOG_LEVEL', default='INFO')),
        event_level=getattr(logging, env.str('SENTRY_EVENT_LEVEL', default='ERROR')),
    )

    sentry_sdk.init(
        dsn=env.str('SENTRY_DSN', default=''),
        environment=env.str('SENTRY_ENVIRONMENT', default='development'),
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            logging_integration,
        ],
        send_default_pii=True,
    )

#########
# DATADOG
#########
if USE_DATADOG:
    import datadog
    from ddtrace import config as dd_config

    datadog_service = env.str('DD_SERVICE', default='base_app')
    datadog_environment = env.str('DD_ENV', default='development')
    datadog_version = env.str('DD_VERSION', default='')
    datadog_agent_hostname = env.str('DD_AGENT_SERVICE_HOST', default='localhost')
    datadog_agent_port = env.str('DD_AGENT_SERVICE_PORT', default='8125')
    datadog_statsd_port = env.str('DD_STATSD_SERVICE_PORT', default='8126')
    datadog_tags = env.list('DD_TAGS', default=[])

    dd_tracer.configure(
        enabled=True,
        hostname=datadog_agent_hostname,
        port=datadog_agent_port,
    )
    dd_tracer.set_tags({
        'env': datadog_environment,
        'version': datadog_version,
        **dict(t.split(':') for t in datadog_tags),
    })
    dd_config.analytics_enabled = True
    dd_config.health_metrics_enabled = True
    dd_config.celery['analytics_enabled'] = True
    dd_config.celery['distributed_tracing'] = True
    dd_config.celery['producer_service_name'] = f'{datadog_service}-celery-queue'
    dd_config.celery['worker_service_name'] = f'{datadog_service}-celery'
    dd_config.django['analytics_enabled'] = True
    dd_config.django['cache_service_name'] = f'{datadog_service}-cache'
    dd_config.django['database_service_name_prefix'] = f'{datadog_service}-'
    dd_config.django['service_name'] = datadog_service
    dd_config.postgres['analytics_enabled'] = True
    dd_config.requests['analytics_enabled'] = True

    datadog.initialize(
        statsd_host=datadog_agent_hostname,
        statsd_port=datadog_statsd_port,
        statsd_namespace=datadog_service,
        statsd_constant_tags=datadog_tags,
    )
else:
    dd_tracer.configure(enabled=False)

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
