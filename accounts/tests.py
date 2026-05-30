from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.models import AcademicYear, Company, Department, InternshipPlacement, User
from accounts.services import AnalyticsService
from logbook.models import Attendance, LogEntry


class AnalyticsServiceTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student', password='Pass12345!', role='student')
        self.supervisor = User.objects.create_user(username='supervisor', password='Pass12345!', role='supervisor')
        self.lecturer = User.objects.create_user(username='lecturer', password='Pass12345!', role='lecturer')
        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.company = Company.objects.create(name='Demo Company', address='Kampala')
        self.year = AcademicYear.objects.create(
            name='2025/2026',
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=330),
        )
        self.placement = InternshipPlacement.objects.create(
            student=self.student,
            company=self.company,
            department=self.department,
            academic_year=self.year,
            company_supervisor=self.supervisor,
            university_supervisor=self.lecturer,
            start_date=date.today() - timedelta(days=5),
            end_date=date.today() + timedelta(days=55),
            expected_working_days=10,
        )

    def test_completion_percentage_uses_approved_logs(self):
        LogEntry.objects.create(
            student=self.student,
            placement=self.placement,
            date=date.today(),
            activities='Built a Django view',
            hours_worked=8,
            status='approved',
        )
        LogEntry.objects.create(
            student=self.student,
            placement=self.placement,
            date=date.today() - timedelta(days=1),
            activities='Prepared notes',
            hours_worked=8,
            status='pending',
        )

        self.assertEqual(self.placement.completion_percentage, 10)

    def test_attendance_percentage_counts_present_and_late(self):
        Attendance.objects.create(student=self.student, placement=self.placement, date=date.today(), status='present')
        Attendance.objects.create(
            student=self.student,
            placement=self.placement,
            date=date.today() - timedelta(days=1),
            status='late',
        )
        Attendance.objects.create(
            student=self.student,
            placement=self.placement,
            date=date.today() - timedelta(days=2),
            status='absent',
        )

        self.assertEqual(AnalyticsService.get_attendance_percentage(self.student), 66.67)


class AdminPlacementPageTests(TestCase):
    def test_assign_page_renders_for_admin(self):
        User.objects.create_user(username='student', password='Pass12345!', role='student')
        User.objects.create_user(username='supervisor', password='Pass12345!', role='supervisor')
        User.objects.create_user(username='lecturer', password='Pass12345!', role='lecturer')
        User.objects.create_user(
            username='admin',
            password='Pass12345!',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        Department.objects.create(name='Computer Science', code='CS')
        Company.objects.create(name='Demo Company', address='Kampala')
        AcademicYear.objects.create(
            name='2025/2026',
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=330),
        )

        self.client.login(username='admin', password='Pass12345!')
        response = self.client.get(reverse('placement_create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Assign Internship Placement')

# Create your tests here.
