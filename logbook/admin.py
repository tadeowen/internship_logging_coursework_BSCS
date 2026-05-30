from django.contrib import admin

from .models import Attendance, Feedback, LogEntry, Notification, WeeklyReport


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'hours_worked', 'status', 'reviewed_by')
    list_filter = ('status', 'date')
    search_fields = ('student__username', 'activities', 'skills_learned')


@admin.register(WeeklyReport)
class WeeklyReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'week_start', 'week_end', 'status', 'reviewed_by')
    list_filter = ('status', 'week_start')
    search_fields = ('student__username', 'summary')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'check_in', 'check_out', 'recorded_by')
    list_filter = ('status', 'date')
    search_fields = ('student__username',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'author', 'created_at')
    search_fields = ('student__username', 'author__username', 'comment')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'title', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('recipient__username', 'title', 'message')
