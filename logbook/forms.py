from django import forms
from .models import Attendance, Feedback, LogEntry, WeeklyReport

class LogEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = ['placement', 'date', 'activities', 'skills_learned', 'challenges', 'hours_worked', 'attachment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'activities': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'skills_learned': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'challenges': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'hours_worked': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['placement'].queryset = student.placements.filter(status__in=['planned', 'active'])

class LogEntryApprovalForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = ['supervisor_comment', 'status']
        widgets = {
            'supervisor_comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class WeeklyReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = [
            'placement',
            'week_start',
            'week_end',
            'summary',
            'learning_outcomes',
            'challenges',
            'next_week_plan',
            'attachment',
        ]
        widgets = {
            'week_start': forms.DateInput(attrs={'type': 'date'}),
            'week_end': forms.DateInput(attrs={'type': 'date'}),
            'summary': forms.Textarea(attrs={'rows': 4}),
            'learning_outcomes': forms.Textarea(attrs={'rows': 3}),
            'challenges': forms.Textarea(attrs={'rows': 3}),
            'next_week_plan': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['placement'].queryset = student.placements.filter(status__in=['planned', 'active'])


class WeeklyReportReviewForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = ['status', 'supervisor_comment']
        widgets = {
            'supervisor_comment': forms.Textarea(attrs={'rows': 3}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'placement', 'date', 'status', 'check_in', 'check_out', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in': forms.TimeInput(attrs={'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'type': 'time'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['student', 'placement', 'daily_log', 'weekly_report', 'comment', 'recommendation']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'recommendation': forms.Textarea(attrs={'rows': 3}),
        }
