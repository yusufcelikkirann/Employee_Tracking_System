from __future__ import absolute_import, unicode_literals

# Celery uygulamasını proje genelinde kullan
from .celery import app as celery_app

__all__ = ['celery_app']
