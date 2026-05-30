from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import InternshipPlacement, User

class Evaluation(models.Model):
    EVALUATOR_TYPE = (
        ('supervisor', 'Company Supervisor'),
        ('lecturer', 'University Supervisor'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations')
    placement = models.ForeignKey(
        InternshipPlacement, on_delete=models.CASCADE, null=True, blank=True, related_name='evaluations'
    )
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_evaluations')
    evaluator_type = models.CharField(max_length=20, choices=EVALUATOR_TYPE)
    punctuality = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(20)])
    technical_skills = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(30)])
    communication = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(20)])
    initiative = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(15)])
    teamwork = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(15)])
    comments = models.TextField(blank=True)
    recommendation = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    @property
    def total_score(self):
        return self.punctuality + self.technical_skills + self.communication + self.initiative + self.teamwork

    @property
    def grade(self):
        if self.total_score >= 80:
            return 'Excellent'
        if self.total_score >= 65:
            return 'Very Good'
        if self.total_score >= 50:
            return 'Good'
        return 'Needs Support'

    def clean(self):
        if self.student_id and self.student.role != 'student':
            raise ValidationError('Evaluation target must be a student.')
        if self.placement_id and self.placement.student_id != self.student_id:
            raise ValidationError('The selected placement does not belong to this student.')

    def __str__(self):
        return f"{self.student.username} evaluated by {self.evaluator.username}"


class VisitSchedule(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visit_schedules')
    placement = models.ForeignKey(
        InternshipPlacement, on_delete=models.CASCADE, null=True, blank=True, related_name='visit_schedules'
    )
    university_supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduled_visits')
    visit_date = models.DateField()
    visit_time = models.TimeField(null=True, blank=True)
    agenda = models.TextField()
    outcome = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['visit_date', 'visit_time']

    def clean(self):
        if self.student_id and self.student.role != 'student':
            raise ValidationError('Visit target must be a student.')
        if self.university_supervisor_id and self.university_supervisor.role != 'lecturer':
            raise ValidationError('Visits must be scheduled by a university supervisor.')

    def __str__(self):
        return f"Visit for {self.student.username} on {self.visit_date}"
