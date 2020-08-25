import os

from celery import Celery, signals
from ddtrace import patch_all
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base_app.settings')
if settings.USE_DATADOG and sys.argv[0].endswith('celery'):  # pragma: no cover
    patch_all()
app = Celery('base_app')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


@signals.setup_logging.connect
def disable_celery_logging_override(**kwargs):  # pragma: no cover
    # let Celery use logging configured by Django rather then set up it's own
    pass
