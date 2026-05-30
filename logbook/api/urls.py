from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.LogEntryListCreateView.as_view(), name='log-list-create'),
    path('logs/<int:pk>/', views.LogEntryRetrieveUpdateDestroyView.as_view(), name='log-detail'),
]