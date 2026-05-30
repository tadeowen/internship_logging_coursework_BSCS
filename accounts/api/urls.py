from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('profiles/', views.InternshipProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', views.InternshipProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail'),
]