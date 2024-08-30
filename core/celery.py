from __future__ import absolute_import, unicode_literals
from django.conf import settings
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

app = Celery('core', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['crontab.tasks'])
