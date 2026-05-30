from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, FormView, UpdateView
from django.db.models import Avg, F, Q
from django.core.paginator import Paginator
from .models import AcademicYear, Company, Department, InternshipPlacement, StudentProfile, User, InternshipProfile
from logbook.models import Attendance, LogEntry, WeeklyReport
from evaluation.models import Evaluation
from .decorators import role_required
from .forms import (
    AcademicYearForm,
    CompanyForm,
    DepartmentForm,
    InternshipPlacementForm,
    StudentProfileForm,
    UserLoginForm,
    UserRegistrationForm,
)

class UserLoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

@method_decorator(role_required('admin'), name='dispatch')
class AdminDashboardView(ListView):
    model = User
    template_name = 'accounts/admin_dashboard.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.none()  # We don't need the user list directly

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from accounts.services import AnalyticsService
        
        # Get basic counts
        context['students'] = User.objects.filter(role='student')
        context['supervisors'] = User.objects.filter(role='supervisor')
        context['lecturers'] = User.objects.filter(role='lecturer')
        context['companies'] = Company.objects.all()
        context['departments'] = Department.objects.all()
        context['placements'] = InternshipPlacement.objects.select_related('student', 'company')[:10]
        context.update(AnalyticsService.get_admin_dashboard())
        
        # Get analytics data
        context['evaluation_trends'] = AnalyticsService.get_evaluation_trends()
        context['monthly_activity'] = AnalyticsService.get_monthly_activity()
        
        # Get top performing students with progress
        students = User.objects.filter(role='student')
        top_students = []
        for student in students[:10]:  # Top 10 students
            progress = AnalyticsService.get_internship_progress(student)
            avg_score = Evaluation.objects.filter(student=student).aggregate(
                avg_score=Avg(
                    (F('punctuality') + F('technical_skills') + F('communication') + F('initiative') + F('teamwork')) / 5
                )
            )['avg_score'] or 0
            
            top_students.append({
                'student': student,
                'average_score': round(avg_score, 2),
                'total_evaluations': Evaluation.objects.filter(student=student).count(),
                'progress_percentage': progress
            })
        
        # Sort by average score descending
        top_students.sort(key=lambda x: x['average_score'], reverse=True)
        context['top_students'] = top_students[:5]  # Top 5 for display
        
        # Get recent log entries
        context['recent_logs'] = LogEntry.objects.select_related('student').order_by('-created_at')[:10]
        
        return context

@method_decorator(role_required('student'), name='dispatch')
class StudentDashboardView(ListView):
    model = LogEntry
    template_name = 'accounts/student_dashboard.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return LogEntry.objects.filter(student=self.request.user).order_by('-date')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from accounts.services import AnalyticsService
        
        # Get evaluations
        context['evaluations'] = Evaluation.objects.filter(student=self.request.user)
        context['analytics'] = AnalyticsService.get_student_dashboard(self.request.user)
        context['weekly_reports'] = WeeklyReport.objects.filter(student=self.request.user)[:5]
        
        # Get internship progress
        context['progress_percentage'] = AnalyticsService.get_internship_progress(self.request.user)
        
        # Get evaluation statistics
        evals = Evaluation.objects.filter(student=self.request.user)
        if evals.exists():
            avg_score = evals.aggregate(
                avg_score=Avg(
                    (F('punctuality') + F('technical_skills') + F('communication') + F('initiative') + F('teamwork')) / 5
                )
            )['avg_score'] or 0
            context['average_score'] = round(avg_score, 2)
            context['total_evaluations'] = evals.count()
        else:
            context['average_score'] = 0
            context['total_evaluations'] = 0
        
        return context

@method_decorator(role_required('supervisor'), name='dispatch')
class SupervisorDashboardView(ListView):
    model = User
    template_name = 'accounts/supervisor_dashboard.html'
    context_object_name = 'students'

    def get_queryset(self):
        # Supervisors can only see students assigned to them
        return User.objects.filter(role='student', profile__supervisor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from accounts.services import AnalyticsService
        
        # Get pending logs for students assigned to this supervisor
        students = context['students']
        context['analytics'] = AnalyticsService.get_supervisor_dashboard(self.request.user)
        context['logs'] = LogEntry.objects.filter(
            student__in=students,
            status='pending'
        ).select_related('student').order_by('-date')
        
        # Get evaluation statistics
        context['pending_evaluations'] = Evaluation.objects.filter(
            student__in=students,
            evaluator=self.request.user
        ).count()
        
        # Get recent evaluations by this supervisor
        context['recent_evaluations'] = Evaluation.objects.filter(
            evaluator=self.request.user
        ).select_related('student').order_by('-submitted_at')[:5]
        
        return context

@method_decorator(role_required('lecturer'), name='dispatch')
class LecturerDashboardView(ListView):
    model = User
    template_name = 'accounts/lecturer_dashboard.html'
    context_object_name = 'students'

    def get_queryset(self):
        # Lecturers can only see students assigned to them
        return User.objects.filter(role='student', profile__lecturer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from accounts.services import AnalyticsService
        
        # Get students assigned to this lecturer
        students = context['students']
        context['visit_schedules'] = self.request.user.scheduled_visits.select_related('student')[:5]
        context['weekly_reports'] = WeeklyReport.objects.filter(student__in=students).select_related('student')[:10]
        
        # Get pending evaluations for students assigned to this lecturer
        context['pending_assessments'] = Evaluation.objects.filter(
            student__in=students,
            evaluator_type='lecturer'
        ).exclude(
            evaluator=self.request.user
        ).count()
        
        # Get evaluation statistics for this lecturer
        context['total_evaluations_given'] = Evaluation.objects.filter(
            evaluator=self.request.user
        ).count()
        
        # Get average score given by this lecturer
        evals_given = Evaluation.objects.filter(evaluator=self.request.user)
        if evals_given.exists():
            avg_score = evals_given.aggregate(
                avg_score=Avg(
                    (F('punctuality') + F('technical_skills') + F('communication') + F('initiative') + F('teamwork')) / 5
                )
            )['avg_score'] or 0
            context['average_score_given'] = round(avg_score, 2)
        else:
            context['average_score_given'] = 0
        
        # Get recent evaluations by this lecturer
        context['recent_evaluations'] = Evaluation.objects.filter(
            evaluator=self.request.user
        ).select_related('student').order_by('-submitted_at')[:5]
        
        return context

@method_decorator(role_required('admin'), name='dispatch')
class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        messages.success(self.request, f'User {form.cleaned_data["username"]} created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'student':
        return redirect('student_dashboard')
    elif request.user.role == 'supervisor':
        return redirect('supervisor_dashboard')
    elif request.user.role == 'lecturer':
        return redirect('lecturer_dashboard')
    return redirect('login')


@method_decorator(role_required('student'), name='dispatch')
class StudentProfileView(UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('student_dashboard')

    def get_object(self, queryset=None):
        obj, _ = StudentProfile.objects.get_or_create(
            student=self.request.user,
            defaults={
                'registration_number': f'TEMP-{self.request.user.id}',
                'programme': 'Computer Science',
                'department': Department.objects.first() or Department.objects.create(name='Computer Science', code='CS'),
            },
        )
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Profile saved successfully.')
        return super().form_valid(form)


@method_decorator(role_required('admin'), name='dispatch')
class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'accounts/simple_form.html'
    success_url = reverse_lazy('admin_dashboard')
    page_title = 'Add Company'


@method_decorator(role_required('admin'), name='dispatch')
class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'accounts/simple_form.html'
    success_url = reverse_lazy('admin_dashboard')
    page_title = 'Add Department'


@method_decorator(role_required('admin'), name='dispatch')
class AcademicYearCreateView(CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'accounts/simple_form.html'
    success_url = reverse_lazy('admin_dashboard')
    page_title = 'Add Academic Year'


@method_decorator(role_required('admin'), name='dispatch')
class PlacementCreateView(CreateView):
    model = InternshipPlacement
    form_class = InternshipPlacementForm
    template_name = 'accounts/simple_form.html'
    success_url = reverse_lazy('admin_dashboard')
    page_title = 'Assign Internship Placement'

    def form_valid(self, form):
        messages.success(self.request, 'Internship placement assigned successfully.')
        return super().form_valid(form)
