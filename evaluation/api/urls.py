from django.urls import path
from . import views

urlpatterns = [
    path('evaluations/', views.EvaluationListCreateView.as_view(), name='evaluation-list-create'),
    path('evaluations/<int:pk>/', views.EvaluationRetrieveUpdateDestroyView.as_view(), name='evaluation-detail'),
]