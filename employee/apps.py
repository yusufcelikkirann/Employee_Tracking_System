# employee/apps.py

from django.apps import AppConfig

class EmployeeConfig(AppConfig):
    name = 'employee'

    def ready(self):
        import employee.signals  # Sinyalleri buradan import ediyoruz
