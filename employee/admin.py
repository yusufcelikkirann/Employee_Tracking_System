from django.contrib import admin
from .models import CustomUser, Attendance, LeaveRequest

# Customize CustomUser admin interface
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'annual_leave')  # Liste görünümü
    list_filter = ('role',)  # Filtreleme
    search_fields = ('username', 'email')  # Arama
    ordering = ('username',)  # Sıralama

    # Alanlar (tüm mevcut bilgiler ve şifre belirleme)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Kullanıcı adı ve şifre
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),  # Kişisel bilgiler
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),  # Yetkiler
        ('Other Info', {'fields': ('annual_leave', 'last_login', 'date_joined')}),  # Diğer bilgiler
    )

    # Şifreyi hash'lemek için save_model metodu
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:  # Eğer şifre alanı değiştirildiyse
            obj.set_password(obj.password)  # Şifreyi hash'le
        super().save_model(request, obj, form, change)

from django.contrib import admin
from .models import Attendance


from django.contrib import admin
from .models import Attendance, LeaveRequest

# Attendance modelini admin paneline kaydediyoruz
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'clock_in_time', 'clock_out_time', 'is_late', 'late_minutes', 'date')  # Correctly separated fields
    search_fields = ('user__username', 'user__email')
    list_filter = ('is_late', 'date')

# LeaveRequest modelini admin paneline kaydediyoruz
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'status')
    search_fields = ('user__username', 'user__email')
    list_filter = ('status', 'start_date', 'end_date')

# Register the models
admin.site.register(CustomUser, CustomUserAdmin)


from django.contrib import admin
from .models import SystemSettings

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('work_start_time', 'work_end_time', 'weekend_days')




