# myapp/middleware.py

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        
        response['Cache-Control'] = 'no-store'
        return response
