# employee_tracking/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django ayarlarını kullan
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_tracking.settings')

app = Celery('employee_tracking')

# Celery'nin Django ile entegre olmasını sağlar
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tüm Django uygulamaları içindeki task'ları yükler
app.autodiscover_tasks()
