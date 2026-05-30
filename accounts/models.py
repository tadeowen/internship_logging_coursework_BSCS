from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('supervisor', 'Company Supervisor'),
        ('lecturer', 'University Supervisor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def full_name(self):
        return self.get_full_name() or self.username


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField()
    contact_person = models.CharField(max_length=120, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    industry = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text='Example: 2025/2026')
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('Academic year end date must be after start date.')

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.CharField(max_length=40, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='students')
    programme = models.CharField(max_length=150)
    year_of_study = models.PositiveSmallIntegerField(default=3)
    emergency_contact = models.CharField(max_length=120, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['registration_number']

    def clean(self):
        if self.student_id and self.student.role != 'student':
            raise ValidationError('Student profile can only be attached to a student user.')

    def __str__(self):
        return f"{self.registration_number} - {self.student.full_name}"


class InternshipPlacement(models.Model):
    STATUS_CHOICES = (
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='placements')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='placements')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='placements')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='placements')
    company_supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='company_supervisions'
    )
    university_supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='university_supervisions'
    )
    title = models.CharField(max_length=160, default='Industrial Training')
    start_date = models.DateField()
    end_date = models.DateField()
    expected_working_days = models.PositiveIntegerField(default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def clean(self):
        if self.student_id and self.student.role != 'student':
            raise ValidationError('Placement student must have the student role.')
        if self.company_supervisor_id and self.company_supervisor.role != 'supervisor':
            raise ValidationError('Company supervisor must have the company supervisor role.')
        if self.university_supervisor_id and self.university_supervisor.role != 'lecturer':
            raise ValidationError('University supervisor must have the university supervisor role.')
        if self.end_date <= self.start_date:
            raise ValidationError('Placement end date must be after start date.')

    @property
    def duration_days(self):
        return max((self.end_date - self.start_date).days + 1, 0)

    @property
    def elapsed_days(self):
        today = date.today()
        if today < self.start_date:
            return 0
        return min((today - self.start_date).days + 1, self.duration_days)

    @property
    def completion_percentage(self):
        if not self.expected_working_days:
            return 0
        approved_logs = self.daily_logs.filter(status='approved').count()
        return round(min((approved_logs / self.expected_working_days) * 100, 100), 2)

    def __str__(self):
        if self.student_id and self.company_id:
            return f"{self.student.full_name} at {self.company.name}"
        return 'New internship placement'


class InternshipProfile(models.Model):
    """Legacy profile kept for compatibility with the original coursework screens."""
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supervised_students')
    lecturer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_students')
    company_name = models.CharField(max_length=200)
    company_address = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.student.username} @ {self.company_name}"
