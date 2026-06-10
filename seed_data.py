import os
import json
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import authenticate
from django.test import Client
import sys

c = Client()

# Create a test user if not exists
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='testadmin').exists():
    User.objects.create_superuser('testadmin', 'admin@test.com', 'admin123', role='admin')
    print('Created test admin user: testadmin / admin123')

user = authenticate(username='testadmin', password='admin123')
assert user is not None, "Authentication failed"
print(f'Auth OK: {user.username} ({user.role})')

from accounts.models import Department, Company, AcademicYear, StudentProfile, InternshipPlacement, InternshipProfile

dept, _ = Department.objects.get_or_create(code='CS', defaults={'name': 'Computer Science', 'description': 'CS Dept'})
company, _ = Company.objects.get_or_create(name='TechCorp Inc.', defaults={'address': '123 Tech St', 'industry': 'Technology'})
year, _ = AcademicYear.objects.get_or_create(name='2025/2026', defaults={'start_date': '2025-09-01', 'end_date': '2026-06-30', 'is_current': True})

student, _ = User.objects.get_or_create(username='student1', defaults={'email': 'student@test.com', 'role': 'student'})
student.set_password('student123')
student.save()
profile, _ = StudentProfile.objects.get_or_create(student=student, defaults={'registration_number': '2025/CS/001', 'department': dept, 'programme': 'BSc Computer Science', 'year_of_study': 4})

supervisor, _ = User.objects.get_or_create(username='supervisor1', defaults={'email': 'sup@test.com', 'role': 'supervisor'})
supervisor.set_password('sup123')
supervisor.save()
lecturer, _ = User.objects.get_or_create(username='lecturer1', defaults={'email': 'lec@test.com', 'role': 'lecturer'})
lecturer.set_password('lec123')
lecturer.save()

placement, _ = InternshipPlacement.objects.get_or_create(student=student, company=company, department=dept, academic_year=year, defaults={'company_supervisor': supervisor, 'university_supervisor': lecturer, 'start_date': '2025-09-01', 'end_date': '2026-01-30', 'expected_working_days': 60, 'status': 'active'})

from datetime import date, timedelta
for i in range(5):
    d = date(2025, 9, 1) + timedelta(days=i)
    _, created = __import__('logbook.models', fromlist=['LogEntry']).LogEntry.objects.get_or_create(student=student, placement=placement, date=d, defaults={'activities': f'Worked on task {i+1}', 'skills_learned': 'Teamwork', 'challenges': 'Time management', 'hours_worked': 8, 'status': 'approved', 'reviewed_by': supervisor})

print('Seed data created successfully')
print('Test accounts:')
print('  Admin:    testadmin / admin123')
print('  Student:  student1 / student123')
print('  Supervisor: supervisor1 / sup123')
print('  Lecturer: lecturer1 / lec123')
