# myapp/middleware.py

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Tüm sayfalara Cache-Control başlıkları ekle
        response['Cache-Control'] = 'no-store'
        return response
