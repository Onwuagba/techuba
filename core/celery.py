from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# create a Celery instance and configure it using the settings from Django
celery_app = Celery('core', broker='sqla+sqlite:///celery_broker.sqlite3')

celery_app.conf.update(
    CELERY_BROKER_URL='sqla+sqlite:///celery_broker.sqlite3',
    CELERY_RESULT_BACKEND='db+sqlite:///celery_backend.sqlite3',
)

# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()