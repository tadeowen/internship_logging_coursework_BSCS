from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('student-dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('supervisor-dashboard/', views.SupervisorDashboardView.as_view(), name='supervisor_dashboard'),
    path('lecturer-dashboard/', views.LecturerDashboardView.as_view(), name='lecturer_dashboard'),
    path('register/', views.UserRegistrationView.as_view(), name='register_user'),
    path('profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('companies/new/', views.CompanyCreateView.as_view(), name='company_create'),
    path('departments/new/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('academic-years/new/', views.AcademicYearCreateView.as_view(), name='academic_year_create'),
    path('placements/new/', views.PlacementCreateView.as_view(), name='placement_create'),
]
