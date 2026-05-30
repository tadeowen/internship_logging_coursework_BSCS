from django.urls import path
from . import views

urlpatterns = [
    path('evaluate/<int:student_id>/', views.EvaluationCreateView.as_view(), name='eval_form'),
    path('results/<int:student_id>/', views.EvaluationResultsView.as_view(), name='results'),
    path('all-evaluations/', views.AllEvaluationsView.as_view(), name='all_evaluations'),
    path('visits/', views.VisitScheduleListView.as_view(), name='visit_schedules'),
    path('visits/new/', views.VisitScheduleCreateView.as_view(), name='visit_create'),
    path('reports/evaluation/<int:student_id>.pdf', views.evaluation_report_pdf, name='evaluation_report_pdf'),
]
