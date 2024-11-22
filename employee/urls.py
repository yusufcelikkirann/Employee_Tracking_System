from django.urls import path
from . import views


urlpatterns = [
    # Genel Giriş ve Çıkış
    path('', views.home, name='home'),  # Home page route
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboardlar
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Clock In/Out İşlemleri
    path('clock_in/', views.clock_in, name='clock_in'),
    path('clock_out/', views.clock_out, name='clock_out'),

    # İzin Talepleri Yönetimi
    path('request_leave/', views.request_leave, name='request_leave'),
    path('manage_leave/', views.manage_leave, name='manage_leave'),
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),

    # Çalışan Yönetimi
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('add_employee/', views.add_employee, name='add_employee'),


     path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('attendance/', views.attendance_list, name='attendance_list'),
    path('notifications/', views.notifications, name='notifications'),

     path('login_employee/', views.employee_login, name='login_employee'),  # Çalışan giriş sayfası
    path('login_admin/', views.admin_login, name='login_admin'),  # Yetkili giriş sayfası
    path('logout/', views.logout_view, name='logout'),

    
]