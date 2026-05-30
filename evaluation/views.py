from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from .models import Evaluation, VisitSchedule
from accounts.models import User
from .forms import EvaluationForm, VisitScheduleForm
from accounts.decorators import role_required

@method_decorator(role_required('supervisor', 'lecturer'), name='dispatch')
class EvaluationCreateView(CreateView):
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'evaluation/eval_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(User, id=kwargs['student_id'], role='student')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.student = self.student
        form.instance.evaluator = self.request.user
        form.instance.evaluator_type = 'supervisor' if self.request.user.role == 'supervisor' else 'lecturer'
        messages.success(self.request, 'Evaluation submitted successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.student
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student'] = self.student
        return kwargs

@method_decorator(role_required('supervisor', 'lecturer'), name='dispatch')
class EvaluationResultsView(ListView):
    model = Evaluation
    template_name = 'evaluation/results.html'
    context_object_name = 'evaluations'

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(User, id=kwargs['student_id'], role='student')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Evaluation.objects.filter(student=self.student)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.student
        return context

@method_decorator(role_required('admin'), name='dispatch')
class AllEvaluationsView(ListView):
    model = Evaluation
    template_name = 'evaluation/all_evaluations.html'
    context_object_name = 'evaluations'
    ordering = ['-submitted_at']


@method_decorator(role_required('lecturer'), name='dispatch')
class VisitScheduleCreateView(CreateView):
    model = VisitSchedule
    form_class = VisitScheduleForm
    template_name = 'evaluation/visit_form.html'
    success_url = reverse_lazy('visit_schedules')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['student'].queryset = User.objects.filter(placements__university_supervisor=self.request.user).distinct()
        return form

    def form_valid(self, form):
        form.instance.university_supervisor = self.request.user
        messages.success(self.request, 'Visit scheduled successfully.')
        return super().form_valid(form)


@method_decorator(role_required('lecturer', 'admin'), name='dispatch')
class VisitScheduleListView(ListView):
    model = VisitSchedule
    template_name = 'evaluation/visit_schedules.html'
    context_object_name = 'visits'
    paginate_by = 15

    def get_queryset(self):
        queryset = VisitSchedule.objects.select_related('student', 'placement', 'university_supervisor')
        if self.request.user.role == 'lecturer':
            queryset = queryset.filter(university_supervisor=self.request.user)
        return queryset


@login_required
def evaluation_report_pdf(request, student_id):
    student = get_object_or_404(User, pk=student_id, role='student')
    evaluations = Evaluation.objects.filter(student=student)
    lines = [f"{evaluation.evaluator.full_name}: {evaluation.total_score}/100 - {evaluation.grade}" for evaluation in evaluations]
    text = f"Evaluation Report - {student.full_name}\n\n" + "\n".join(lines or ['No evaluations submitted yet.'])
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
    return HttpResponse(pdf, content_type='application/pdf')
