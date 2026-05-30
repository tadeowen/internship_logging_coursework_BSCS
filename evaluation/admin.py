from django.contrib import admin

from .models import Evaluation, VisitSchedule


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student', 'evaluator', 'evaluator_type', 'total_score', 'submitted_at')
    list_filter = ('evaluator_type', 'submitted_at')
    search_fields = ('student__username', 'evaluator__username', 'comments')


@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ('student', 'university_supervisor', 'visit_date', 'visit_time', 'status')
    list_filter = ('status', 'visit_date')
    search_fields = ('student__username', 'university_supervisor__username', 'agenda')
