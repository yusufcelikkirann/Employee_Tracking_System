from django.contrib import admin
from .models import CustomUser, Attendance, LeaveRequest
from django.contrib import admin
from .models import Attendance
from django.contrib import admin
from .models import SystemSettings
from django.contrib import admin
from .models import Attendance, LeaveRequest


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'annual_leave')  
    list_filter = ('role',)  
    search_fields = ('username', 'email')  
    ordering = ('username',)  

   
    fieldsets = (
        (None, {'fields': ('username', 'password')}), 
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),  
        ('Other Info', {'fields': ('annual_leave', 'last_login', 'date_joined')}), 
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:  
            obj.set_password(obj.password) 
        super().save_model(request, obj, form, change)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'clock_in_time', 'clock_out_time', 'is_late', 'late_minutes', 'date') 
    search_fields = ('user__username', 'user__email')
    list_filter = ('is_late', 'date')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'status')
    search_fields = ('user__username', 'user__email')
    list_filter = ('status', 'start_date', 'end_date')

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('work_start_time', 'work_end_time', 'weekend_days')




