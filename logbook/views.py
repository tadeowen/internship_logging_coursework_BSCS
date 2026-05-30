from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, ListView
from .models import Attendance, Feedback, LogEntry, WeeklyReport
from accounts.models import User
from .forms import AttendanceForm, FeedbackForm, LogEntryForm, LogEntryApprovalForm, WeeklyReportForm, WeeklyReportReviewForm
from accounts.decorators import role_required

@method_decorator(role_required('student'), name='dispatch')
class SubmitLogView(CreateView):
    model = LogEntry
    form_class = LogEntryForm
    template_name = 'logbook/log_form.html'
    success_url = reverse_lazy('my_logs')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.status = 'pending'
        messages.success(self.request, 'Log entry submitted successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

@method_decorator(role_required('supervisor'), name='dispatch')
class ApproveLogView(UpdateView):
    model = LogEntry
    form_class = LogEntryApprovalForm
    template_name = 'logbook/approve_log.html'
    success_url = reverse_lazy('supervisor_dashboard')

    def get_queryset(self):
        return LogEntry.objects.filter(student__placements__company_supervisor=self.request.user).distinct()

    def form_valid(self, form):
        form.instance.mark_reviewed(self.request.user)
        messages.success(self.request, 'Log entry reviewed successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

@method_decorator(role_required('student'), name='dispatch')
class MyLogsView(ListView):
    model = LogEntry
    template_name = 'logbook/my_logs.html'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self):
        queryset = LogEntry.objects.filter(student=self.request.user)
        status = self.request.GET.get('status')
        query = self.request.GET.get('q')
        if status:
            queryset = queryset.filter(status=status)
        if query:
            queryset = queryset.filter(activities__icontains=query)
        return queryset

@method_decorator(role_required('admin', 'supervisor', 'lecturer'), name='dispatch')
class AllLogsView(ListView):
    model = LogEntry
    template_name = 'logbook/all_logs.html'
    context_object_name = 'logs'
    ordering = ['-date']
    paginate_by = 15

    def get_queryset(self):
        queryset = LogEntry.objects.select_related('student', 'placement')
        if self.request.user.role == 'supervisor':
            queryset = queryset.filter(student__placements__company_supervisor=self.request.user)
        elif self.request.user.role == 'lecturer':
            queryset = queryset.filter(student__placements__university_supervisor=self.request.user)
        status = self.request.GET.get('status')
        query = self.request.GET.get('q')
        if status:
            queryset = queryset.filter(status=status)
        if query:
            queryset = queryset.filter(student__username__icontains=query)
        return queryset.distinct().order_by('-date')


@method_decorator(role_required('student'), name='dispatch')
class WeeklyReportCreateView(CreateView):
    model = WeeklyReport
    form_class = WeeklyReportForm
    template_name = 'logbook/weekly_report_form.html'
    success_url = reverse_lazy('weekly_reports')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.student = self.request.user
        messages.success(self.request, 'Weekly report submitted successfully.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class WeeklyReportListView(ListView):
    model = WeeklyReport
    template_name = 'logbook/weekly_reports.html'
    context_object_name = 'reports'
    paginate_by = 10

    def get_queryset(self):
        queryset = WeeklyReport.objects.select_related('student', 'placement')
        if self.request.user.role == 'student':
            queryset = queryset.filter(student=self.request.user)
        elif self.request.user.role == 'supervisor':
            queryset = queryset.filter(student__placements__company_supervisor=self.request.user)
        elif self.request.user.role == 'lecturer':
            queryset = queryset.filter(student__placements__university_supervisor=self.request.user)
        return queryset.distinct()


@method_decorator(role_required('supervisor', 'lecturer'), name='dispatch')
class WeeklyReportReviewView(UpdateView):
    model = WeeklyReport
    form_class = WeeklyReportReviewForm
    template_name = 'logbook/weekly_report_review.html'
    success_url = reverse_lazy('weekly_reports')

    def get_queryset(self):
        if self.request.user.role == 'supervisor':
            return WeeklyReport.objects.filter(student__placements__company_supervisor=self.request.user).distinct()
        return WeeklyReport.objects.filter(student__placements__university_supervisor=self.request.user).distinct()

    def form_valid(self, form):
        form.instance.reviewed_by = self.request.user
        messages.success(self.request, 'Weekly report reviewed successfully.')
        return super().form_valid(form)


@method_decorator(role_required('admin', 'supervisor'), name='dispatch')
class AttendanceCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'logbook/attendance_form.html'
    success_url = reverse_lazy('attendance')

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, 'Attendance recorded successfully.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AttendanceListView(ListView):
    model = Attendance
    template_name = 'logbook/attendance.html'
    context_object_name = 'attendance_records'
    paginate_by = 15

    def get_queryset(self):
        queryset = Attendance.objects.select_related('student', 'placement')
        if self.request.user.role == 'student':
            queryset = queryset.filter(student=self.request.user)
        elif self.request.user.role == 'supervisor':
            queryset = queryset.filter(student__placements__company_supervisor=self.request.user)
        elif self.request.user.role == 'lecturer':
            queryset = queryset.filter(student__placements__university_supervisor=self.request.user)
        return queryset.distinct()


def _simple_pdf(title, lines):
    text = title + "\n\n" + "\n".join(lines)
    stream = f"BT /F1 12 Tf 50 760 Td ({text[:1500].replace('(', '[').replace(')', ']')}) Tj ET"
    pdf = (
        "%PDF-1.4\n"
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
        "4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
        f"5 0 obj << /Length {len(stream)} >> stream\n{stream}\nendstream endobj\n"
        "trailer << /Root 1 0 R >>\n%%EOF"
    )
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title.lower().replace(" ", "_")}.pdf"'
    return response


@login_required
def generate_logbook_pdf(request):
    student = request.user
    if request.user.role != 'student':
        student = get_object_or_404(User, pk=request.GET.get('student_id'), role='student')
    logs = LogEntry.objects.filter(student=student).order_by('date')
    lines = [f"{log.date}: {log.activities[:90]} ({log.status})" for log in logs]
    return _simple_pdf(f"Internship Logbook - {student.full_name}", lines or ['No daily logs submitted yet.'])


@login_required
def attendance_report_pdf(request):
    student = request.user
    if request.user.role != 'student' and request.GET.get('student_id'):
        student = get_object_or_404(User, pk=request.GET.get('student_id'), role='student')
    records = Attendance.objects.filter(student=student).order_by('date')
    total = records.count()
    present = records.filter(status__in=['present', 'late']).count()
    percentage = round((present / total) * 100, 2) if total else 0
    lines = [f"Attendance: {percentage}% ({present}/{total})"]
    lines.extend([f"{record.date}: {record.status}" for record in records])
    return _simple_pdf(f"Attendance Report - {student.full_name}", lines)
