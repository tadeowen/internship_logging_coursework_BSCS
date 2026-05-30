# Internship Logging and Management System

A Django 5-style MTV coursework project for managing university internship logs, reports, attendance, supervisor feedback, visits, and evaluations.

## Main Modules

- `accounts`: custom user roles, departments, companies, academic years, student profiles, placements, dashboards, and access control.
- `logbook`: daily logs, weekly reports, attendance, feedback, notifications, uploads, and PDF-style downloads.
- `evaluation`: supervisor evaluations, university visit schedules, and evaluation reports.
- `templates`: shared responsive Bootstrap 5 layout.

## Database Schema

Core entities:

- `User`: authentication account with role: student, company supervisor, university supervisor, or admin.
- `StudentProfile`: one-to-one academic profile for a student.
- `Department`, `Company`, `AcademicYear`: institutional reference data.
- `InternshipPlacement`: connects a student to a company, supervisors, department, academic year, and dates.
- `LogEntry` / `DailyLog`: daily internship activities with approval workflow and upload support.
- `WeeklyReport`: weekly summary with upload support and supervisor review.
- `Attendance`: daily presence tracking.
- `Feedback`: comments tied to logs or reports.
- `Evaluation`: scored supervisor/university evaluation.
- `VisitSchedule`: university supervisor visit planning.
- `Notification`: review status messages for students.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install django djangorestframework psycopg2-binary
python manage.py makemigrations
python manage.py migrate
python manage.py seed_sample_data
python manage.py runserver
```

Sample logins after seeding:

- `admin` / `Pass12345!`
- `student1` / `Pass12345!`
- `supervisor1` / `Pass12345!`
- `lecturer1` / `Pass12345!`

## Development Database

SQLite is used automatically when no production database environment variables are set.

## PostgreSQL Deployment

Set these environment variables in production:

```bash
SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres
POSTGRES_DB=internship_system
POSTGRES_USER=internship_user
POSTGRES_PASSWORD=strong-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

Then run:

```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

Use Gunicorn plus Nginx or a platform such as Render, Railway, Fly.io, or Heroku-compatible hosting.

## Testing Procedure

```bash
python manage.py check
python manage.py test
```

Manual assessment checklist:

- Register users as admin and confirm role-based dashboard redirects.
- Create company, department, academic year, and internship placement.
- Log in as a student, update profile, submit daily logs and weekly reports with attachments.
- Log in as company supervisor, review pending logs, record attendance, and evaluate a student.
- Log in as university supervisor, review reports, schedule a visit, and add evaluation recommendations.
- Log in as admin, inspect analytics counts, all logs, all evaluations, and Django admin records.
- Download logbook, attendance, and evaluation reports.

## Algorithms Demonstrated

- Internship completion percentage: approved logs divided by expected working days.
- Attendance percentage: present/late attendance divided by total attendance records.
- Supervisor assignment: placements connect students to company and university supervisors.
- Dashboard analytics: counts and aggregations across users, placements, logs, attendance, reports, and evaluations.
- Report generation: report endpoints convert database records into downloadable PDF responses.
