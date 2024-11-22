from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime, time
from django.utils.timezone import now
from .tasks import notify_admin_of_late_employee

# Kullanıcı Modeli
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('EMPLOYEE', 'Employee'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
    annual_leave = models.IntegerField(default=15)

    # Override groups and user_permissions fields to resolve conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# Attendance Model (Clock In/Out)
class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField(null=True, blank=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    late_minutes = models.IntegerField(default=0)
    date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.clock_in_time:
            self.late_minutes = calculate_late_minutes(self.clock_in_time)
            self.is_late = self.late_minutes > 0
            self.date = self.clock_in_time.date()

            # Notify if the employee is late
            if self.is_late:
                notify_admin_of_late_employee.delay(self.user.id, self.late_minutes)

        super().save(*args, **kwargs)

    def reset_daily_attendance(self):
        """Resets attendance for the next day."""
        today = now().date()
        if self.date and self.date < today:
            self.clock_in_time = None
            self.clock_out_time = None
            self.is_late = False
            self.late_minutes = 0
            self.date = today
            self.save()

    @property
    def worked_hours(self):
        """Calculate hours worked based on clock-in and clock-out times."""
        if self.clock_in_time and self.clock_out_time:
            delta = self.clock_out_time - self.clock_in_time
            return delta.total_seconds() / 3600  # Returns hours worked
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.date}"


# Calculate Late Minutes
def calculate_late_minutes(clock_in_time):
    from .models import SystemSettings  # Import to avoid circular imports
    settings = SystemSettings.objects.first() or SystemSettings()  # Default to empty if no settings found

    work_start = time(settings.work_start_time, 0)

    if clock_in_time.time() > work_start:
        late_duration = datetime.combine(clock_in_time.date(), clock_in_time.time()) - \
                        datetime.combine(clock_in_time.date(), work_start)
        return late_duration.seconds // 60  # Return late minutes
    return 0


# SystemSettings Model (Work Schedule Configuration)
class SystemSettings(models.Model):
    work_start_time = models.IntegerField(default=8)  # Work start time (08:00)
    work_end_time = models.IntegerField(default=18)   # Work end time (18:00)
    weekend_days = models.CharField(max_length=50, default='5,6')  # Saturday and Sunday (0 = Monday)

    def get_weekend_days(self):
        """Returns weekend days as a list of integers."""
        return list(map(int, self.weekend_days.split(',')))

    def save(self, *args, **kwargs):
        """Save weekend_days in correct format."""
        if isinstance(self.weekend_days, list):
            self.weekend_days = ','.join(map(str, self.weekend_days))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"System Settings: {self.work_start_time} - {self.work_end_time}"


# LeaveRequest Model
class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('PENDING', 'Pending'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date} ({self.get_status_display()})"
