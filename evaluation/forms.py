from django import forms
from .models import Evaluation, VisitSchedule

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'placement',
            'punctuality',
            'technical_skills',
            'communication',
            'initiative',
            'teamwork',
            'comments',
            'recommendation',
        ]
        widgets = {
            'punctuality': forms.NumberInput(attrs={'min': 0, 'max': 20, 'class': 'form-control'}),
            'technical_skills': forms.NumberInput(attrs={'min': 0, 'max': 30, 'class': 'form-control'}),
            'communication': forms.NumberInput(attrs={'min': 0, 'max': 20, 'class': 'form-control'}),
            'initiative': forms.NumberInput(attrs={'min': 0, 'max': 15, 'class': 'form-control'}),
            'teamwork': forms.NumberInput(attrs={'min': 0, 'max': 15, 'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'recommendation': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['placement'].queryset = student.placements.all()


class VisitScheduleForm(forms.ModelForm):
    class Meta:
        model = VisitSchedule
        fields = ['student', 'placement', 'visit_date', 'visit_time', 'agenda', 'status', 'outcome']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'visit_time': forms.TimeInput(attrs={'type': 'time'}),
            'agenda': forms.Textarea(attrs={'rows': 3}),
            'outcome': forms.Textarea(attrs={'rows': 3}),
        }
