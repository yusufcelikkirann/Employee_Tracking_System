from rest_framework import serializers
from .models import CustomUser, Attendance, SystemSettings, LeaveRequest

# CustomUser Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'annual_leave']

# Attendance Serializer
class AttendanceSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'clock_in_time', 'clock_out_time', 'is_late', 'late_minutes', 'worked_hours', 'date']

# SystemSettings Serializer
class SystemSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSettings
        fields = ['id', 'work_start_time', 'work_end_time', 'weekend_days']

# LeaveRequest Serializer
class LeaveRequestSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = LeaveRequest
        fields = ['id', 'user', 'start_date', 'end_date', 'status']
