from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from .models import CustomUser, Attendance, LeaveRequest
from .forms import EmployeeForm
import logging

logger = logging.getLogger(__name__)

# Home View
def home(request):
    return render(request, 'employee/home.html')  # Ana sayfa

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'EMPLOYEE':
                return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'employee/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Admin Dashboard View
from .models import Attendance  # Attendance modelini içe aktarın
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, LeaveRequest, Attendance
import logging

logger = logging.getLogger(__name__)

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('employee_dashboard')

    employees = CustomUser.objects.filter(role='EMPLOYEE')
    leave_requests = LeaveRequest.objects.all().order_by('-start_date')

    # İzin gün sayısını hesapla ve ekle
    for leave_request in leave_requests:
        leave_request.leave_days = (leave_request.end_date - leave_request.start_date).days + 1

    # Late attendance kayıtlarını alıyoruz
    late_attendances = Attendance.objects.filter(is_late=True).order_by('-date')

    # Debug log
    for leave in leave_requests:
        logger.info(f"Leave Request: {leave.user.username}, Status: {leave.status}")
    for attendance in late_attendances:
        logger.info(f"Late Attendance: {attendance.user.username}, Date: {attendance.date}, Late Minutes: {attendance.late_minutes}")

    return render(request, 'employee/admin_dashboard.html', {
        'employees': employees,
        'leave_requests': leave_requests,
        'late_attendances': late_attendances,  # Late attendance ekleniyor
    })






@login_required
def employee_dashboard(request):
    if request.user.role != 'EMPLOYEE':
        return redirect('admin_dashboard')

    leave_requests = LeaveRequest.objects.filter(user=request.user).order_by('-start_date')

    # Her izin talebi için leave_days hesaplayalım
    for leave_request in leave_requests:
        leave_request.leave_days = (leave_request.end_date - leave_request.start_date).days + 1

    attendance_records = Attendance.objects.filter(user=request.user).order_by('-date')[:5]

    context = {
        'leave_requests': leave_requests,
        'attendance_records': attendance_records,
        'annual_leave': request.user.annual_leave,
    }
    return render(request, 'employee/employee_dashboard.html', context)


@login_required
def clock_in(request):
    today = now().date()
    attendance, created = Attendance.objects.get_or_create(user=request.user)

    # Günlük sıfırlama kontrolü
    attendance.reset_daily_attendance()

    if attendance.clock_in_time is None:
        attendance.clock_in_time = now()
        attendance.save()
        messages.success(request, "Clock-in başarılı!")
    else:
        messages.error(request, "Bugün zaten clock-in yaptınız.")

    return redirect('employee_dashboard')


# Clock Out View
@login_required
def clock_out(request):
    today = now().date()
    attendance = Attendance.objects.filter(user=request.user, date=today).first()

    if attendance:
        if attendance.clock_out_time is None:
            attendance.clock_out_time = now()
            attendance.save()
            messages.success(request, "Clock-out başarılı!")
        else:
            messages.error(request, "Bugün zaten clock-out yaptınız.")
    else:
        messages.error(request, "Önce clock-in yapmalısınız.")

    return redirect('employee_dashboard')

# Request Leave View
@login_required
def request_leave(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        leave_days = (now().date() - now().date()).days + 1
        if leave_days > request.user.annual_leave:
            messages.warning(request, "You don't have enough annual leave!")
            return redirect('employee_dashboard')

        LeaveRequest.objects.create(
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            status='PENDING'
        )
        messages.success(request, "Leave request submitted!")
        return redirect('employee_dashboard')

    return render(request, 'employee/leave_request.html')

# Manage Leave View (Admin)
@login_required
def manage_leave(request):
    if request.user.role != 'ADMIN':
        return redirect('employee_dashboard')

    leave_requests = LeaveRequest.objects.filter(status='PENDING').order_by('-start_date')
    return render(request, 'employee/manage_leave.html', {'leave_requests': leave_requests})

from datetime import timedelta

from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum

@login_required
def approve_leave(request, leave_id):
    if request.user.role != 'ADMIN':
        return redirect('employee_dashboard')

    leave_request = get_object_or_404(LeaveRequest, id=leave_id)

    # Başlangıç ve bitiş tarihleri arasındaki gün sayısını hesapla
    leave_days = (leave_request.end_date - leave_request.start_date).days + 1

    # Kullanıcının geç kaldığı dakika bilgilerini al
    late_minutes = Attendance.objects.filter(user=leave_request.user, is_late=True).aggregate(total_late_minutes=Sum('late_minutes'))['total_late_minutes'] or 0

    # Geç kalan dakikayı günlere çevirelim
    late_days = late_minutes / 1440  # 1 gün = 1440 dakika

    # İzin günlerinden geç kalan günleri düş
    leave_days -= late_days

    # Eğer kullanıcının yıllık izni yeterliyse
    if leave_request.user.annual_leave >= leave_days:
        leave_request.user.annual_leave -= leave_days
        leave_request.user.save()  # Kullanıcıyı kaydet
        leave_request.status = 'APPROVED'
        leave_request.save()  # İzin talebini kaydet
        messages.success(request, f"Leave request approved! Total leave days after deduction: {leave_days}")
    else:
        messages.warning(request, "Not enough annual leave to approve the request.")

    return redirect('admin_dashboard')




# Reject Leave
@login_required
def reject_leave(request, leave_id):
    if request.user.role != 'ADMIN':
        return redirect('employee_dashboard')

    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    leave_request.status = 'REJECTED'
    leave_request.save()
    messages.success(request, "Leave request rejected!")
    return redirect('admin_dashboard')

# Employee Management Views
@login_required
def edit_employee(request, employee_id):
    if request.user.role != 'ADMIN':
        return redirect('employee_dashboard')

    employee = get_object_or_404(CustomUser, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee details updated!")
            return redirect('admin_dashboard')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee/edit_employee.html', {'form': form})

@login_required
def delete_employee(request, employee_id):
    if request.user.role != 'ADMIN':
        return redirect('employee_dashboard')

    employee = get_object_or_404(CustomUser, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect('admin_dashboard')
    return render(request, 'employee/confirm_delete.html', {'employee': employee})

@login_required
def add_employee(request):
    if request.user.role != 'ADMIN':
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New employee added successfully!")
            return redirect('admin_dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'employee/add_employee.html', {'form': form})




from django.shortcuts import render
from .models import Attendance

def attendance_list(request):
    attendance_list = Attendance.objects.all()
    return render(request, 'employee/attendance_list.html', {'attendance_list': attendance_list})



def notifications(request):
    return render(request, 'notifications.html')


from django.utils.timezone import now
from .models import Attendance

def reset_all_attendance():
    today = now().date()
    Attendance.objects.filter(date__lt=today).update(
        clock_in_time=None,
        clock_out_time=None,
        is_late=False,
        late_minutes=0,
        date=today,
    )



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Çalışan Giriş Sayfası
def employee_login(request):
    if request.method == 'POST':
        # Burada çalışan için giriş kontrolünü yapabilirsiniz
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'EMPLOYEE':  # Eğer kullanıcı çalışan ise
            login(request, user)
            return redirect('employee_dashboard')  # Çalışan dashboard'a yönlendir
        else:
            messages.error(request, "Giriş yetkisine sahip değilsiniz!")
            pass
    return render(request, 'employee/login_employee.html')  # Çalışan giriş sayfası

# Yetkili Giriş Sayfası
def admin_login(request):
    if request.method == 'POST':
        # Burada yetkili için giriş kontrolünü yapabilirsiniz
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'ADMIN':  # Eğer kullanıcı yetkili ise
            login(request, user)
            return redirect('admin_dashboard')  # Admin dashboard'a yönlendir
        else:
            messages.error(request, "Giriş yetkisine sahip değilsiniz!")
            pass

    return render(request, 'employee/login_admin.html')  # Yetkili giriş sayfası


# Çıkış işlemi
def logout_view(request):
    logout(request)
    return redirect('login')  # Giriş sayfasına yönlendir


from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import Now

# Çalışan için o ayki çalışma saatlerini hesapla
def calculate_work_hours(user, month, year):
    # Kullanıcının o ayda yaptığı tüm çalışmaları al
    attendance_records = Attendance.objects.filter(
        user=user,
        clock_in_time__year=year,
        clock_in_time__month=month
    )

    total_minutes = 0
    for record in attendance_records:
        if record.clock_in_time and record.clock_out_time:
            # Geçerli gün için geçen süreyi dakika olarak hesaplayalım
            worked_duration = record.clock_out_time - record.clock_in_time
            total_minutes += worked_duration.total_seconds() / 60  # dakika cinsinden

    total_hours = total_minutes / 60  # toplam saat
    return total_hours


from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import Attendance, CustomUser

@login_required
def monthly_report(request):
    # Bu ayı alalım
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    # Tüm çalışanları alalım
    employees = CustomUser.objects.filter(role='EMPLOYEE')

    # Her bir çalışanın aylık çalışma saatlerini hesaplayalım
    report_data = []
    for employee in employees:
        total_hours = calculate_work_hours(employee, current_month, current_year)
        report_data.append({
            'employee': employee,
            'total_hours': total_hours
        })

    return render(request, 'employee/monthly_report.html', {
        'report_data': report_data,
        'month': today.strftime('%B %Y')
    })






from rest_framework import viewsets
from .models import CustomUser, Attendance, SystemSettings, LeaveRequest
from .serializers import CustomUserSerializer, AttendanceSerializer, SystemSettingsSerializer, LeaveRequestSerializer

# CustomUser ViewSet
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# Attendance ViewSet
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

# SystemSettings ViewSet
class SystemSettingsViewSet(viewsets.ModelViewSet):
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer

# LeaveRequest ViewSet
class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer



# employee/views.py
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
)
