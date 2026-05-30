from django.urls import path
from . import views

urlpatterns = [
    path('my-logs/', views.MyLogsView.as_view(), name='my_logs'),
    path('submit-log/', views.SubmitLogView.as_view(), name='submit_log'),
    path('approve-log/<int:pk>/', views.ApproveLogView.as_view(), name='approve_log'),
    path('all-logs/', views.AllLogsView.as_view(), name='all_logs'),
    path('weekly-reports/', views.WeeklyReportListView.as_view(), name='weekly_reports'),
    path('weekly-reports/new/', views.WeeklyReportCreateView.as_view(), name='weekly_report_create'),
    path('weekly-reports/<int:pk>/review/', views.WeeklyReportReviewView.as_view(), name='weekly_report_review'),
    path('attendance/', views.AttendanceListView.as_view(), name='attendance'),
    path('attendance/new/', views.AttendanceCreateView.as_view(), name='attendance_create'),
    path('reports/logbook.pdf', views.generate_logbook_pdf, name='logbook_pdf'),
    path('reports/attendance.pdf', views.attendance_report_pdf, name='attendance_report_pdf'),
]
