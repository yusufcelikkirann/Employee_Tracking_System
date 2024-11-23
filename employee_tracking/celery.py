from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings modülünü tanımlayın
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_tracking.settings')

# Celery uygulamasını başlatın
app = Celery('employee_tracking')

# Celery'nin Django ayarlarını kullanmasını sağlamak için
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery'nin Django'daki task'ları keşfetmesini sağlayın
app.autodiscover_tasks()

from celery import Celery

app = Celery('employee_tracking', broker='redis://localhost:6379/0')