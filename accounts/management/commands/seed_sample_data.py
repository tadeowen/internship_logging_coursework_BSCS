from datetime import date, timedelta

from django.core.management.base import BaseCommand

from accounts.models import AcademicYear, Company, Department, InternshipPlacement, StudentProfile, User
from evaluation.models import Evaluation, VisitSchedule
from logbook.models import Attendance, LogEntry, WeeklyReport


class Command(BaseCommand):
    help = 'Create sample users, placements, logs, attendance, reports, visits, and evaluations.'

    def handle(self, *args, **options):
        department, _ = Department.objects.get_or_create(
            code='CS',
            defaults={'name': 'Computer Science', 'description': 'Computing and software engineering programmes.'},
        )
        company, _ = Company.objects.get_or_create(
            name='TechLabs Uganda',
            defaults={
                'address': 'Plot 10 Innovation Street, Kampala',
                'contact_person': 'Grace Akello',
                'contact_email': 'grace@techlabs.example',
                'contact_phone': '+256700000001',
                'industry': 'Software Development',
            },
        )
        academic_year, _ = AcademicYear.objects.get_or_create(
            name='2025/2026',
            defaults={'start_date': date(2025, 8, 1), 'end_date': date(2026, 7, 31), 'is_current': True},
        )

        admin = self._user('admin', 'admin', is_staff=True, is_superuser=True)
        student = self._user('student1', 'student')
        supervisor = self._user('supervisor1', 'supervisor')
        lecturer = self._user('lecturer1', 'lecturer')

        StudentProfile.objects.get_or_create(
            student=student,
            defaults={
                'registration_number': 'CS-2026-001',
                'department': department,
                'programme': 'Bachelor of Computer Science',
                'year_of_study': 3,
            },
        )
        placement, _ = InternshipPlacement.objects.get_or_create(
            student=student,
            academic_year=academic_year,
            defaults={
                'company': company,
                'department': department,
                'company_supervisor': supervisor,
                'university_supervisor': lecturer,
                'start_date': date.today() - timedelta(days=14),
                'end_date': date.today() + timedelta(days=46),
                'expected_working_days': 60,
                'status': 'active',
            },
        )

        for index in range(1, 6):
            log_date = date.today() - timedelta(days=6 - index)
            LogEntry.objects.get_or_create(
                student=student,
                date=log_date,
                defaults={
                    'placement': placement,
                    'activities': f'Worked on Django feature {index}, wrote tests, and documented progress.',
                    'skills_learned': 'Django MTV, database queries, teamwork',
                    'hours_worked': 8,
                    'status': 'approved' if index <= 3 else 'pending',
                    'reviewed_by': supervisor if index <= 3 else None,
                },
            )
            Attendance.objects.get_or_create(
                student=student,
                date=log_date,
                defaults={'placement': placement, 'status': 'present', 'recorded_by': supervisor},
            )

        WeeklyReport.objects.get_or_create(
            student=student,
            week_start=date.today() - timedelta(days=7),
            defaults={
                'placement': placement,
                'week_end': date.today() - timedelta(days=1),
                'summary': 'Completed onboarding, learned project workflow, and contributed to a Django module.',
                'learning_outcomes': 'Understood model relationships and review workflows.',
                'status': 'approved',
                'reviewed_by': supervisor,
            },
        )
        Evaluation.objects.get_or_create(
            student=student,
            evaluator=supervisor,
            evaluator_type='supervisor',
            defaults={
                'placement': placement,
                'punctuality': 18,
                'technical_skills': 25,
                'communication': 17,
                'initiative': 13,
                'teamwork': 14,
                'comments': 'Good progress and professional conduct.',
            },
        )
        VisitSchedule.objects.get_or_create(
            student=student,
            university_supervisor=lecturer,
            visit_date=date.today() + timedelta(days=7),
            defaults={'placement': placement, 'agenda': 'Review logbook, discuss learning outcomes, and meet company supervisor.'},
        )

        self.stdout.write(self.style.SUCCESS('Sample data created. Login password for sample users is: Pass12345!'))

    def _user(self, username, role, **flags):
        user, created = User.objects.get_or_create(username=username, defaults={'role': role, **flags})
        if created:
            user.set_password('Pass12345!')
            user.email = f'{username}@example.com'
            user.first_name = username.title()
            user.save()
        return user
