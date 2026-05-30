from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.utils import timezone

from accounts.models import InternshipPlacement, User


def log_upload_path(instance, filename):
    return f"uploads/logs/student_{instance.student_id}/{filename}"


def report_upload_path(instance, filename):
    return f"uploads/reports/student_{instance.student_id}/{filename}"


class LogEntry(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='log_entries')
    placement = models.ForeignKey(
        InternshipPlacement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='daily_logs',
    )
    date = models.DateField()
    activities = models.TextField()
    skills_learned = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    hours_worked = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(24)],
    )
    attachment = models.FileField(
        upload_to=log_upload_path,
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])],
    )
    supervisor_comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_logs'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(fields=['student', 'date'], name='one_log_per_student_per_day')
        ]

    def __str__(self):
        return f"{self.student.username} - {self.date}"

    def clean(self):
        if self.student_id and self.student.role != 'student':
            raise ValidationError('Daily logs can only be created by student users.')
        if self.placement_id and self.placement.student_id != self.student_id:
            raise ValidationError('The selected placement does not belong to this student.')

    def mark_reviewed(self, reviewer):
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()


class DailyLog(LogEntry):
    class Meta:
        proxy = True
        verbose_name = 'Daily log'
        verbose_name_plural = 'Daily logs'


class WeeklyReport(models.Model):
    STATUS_CHOICES = LogEntry.STATUS_CHOICES

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_reports')
    placement = models.ForeignKey(
        InternshipPlacement, on_delete=models.CASCADE, null=True, blank=True, related_name='weekly_reports'
    )
    week_start = models.DateField()
    week_end = models.DateField()
    summary = models.TextField()
    learning_outcomes = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    next_week_plan = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to=report_upload_path,
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])],
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    supervisor_comment = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_weekly_reports'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-week_start']
        constraints = [
            models.UniqueConstraint(fields=['student', 'week_start'], name='one_weekly_report_per_student_week')
        ]

    def clean(self):
        if self.week_end < self.week_start:
            raise ValidationError('Week end date cannot be before week start date.')
        if self.placement_id and self.placement.student_id != self.student_id:
            raise ValidationError('The selected placement does not belong to this student.')

    def __str__(self):
        return f"{self.student.username}: {self.week_start} to {self.week_end}"


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    placement = models.ForeignKey(
        InternshipPlacement, on_delete=models.CASCADE, null=True, blank=True, related_name='attendance_records'
    )
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_attendance'
    )

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(fields=['student', 'date'], name='one_attendance_record_per_student_day')
        ]

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"


class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_received')
    placement = models.ForeignKey(
        InternshipPlacement, on_delete=models.CASCADE, null=True, blank=True, related_name='feedback'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_given')
    daily_log = models.ForeignKey(LogEntry, on_delete=models.CASCADE, null=True, blank=True, related_name='feedback')
    weekly_report = models.ForeignKey(
        WeeklyReport, on_delete=models.CASCADE, null=True, blank=True, related_name='feedback'
    )
    comment = models.TextField()
    recommendation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for {self.student.username} by {self.author.username}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=120)
    message = models.TextField()
    url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
