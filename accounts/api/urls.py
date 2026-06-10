from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('profiles/', views.InternshipProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', views.InternshipProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail'),
    path('placements/', views.PlacementListCreateView.as_view(), name='placement-list-create'),
    path('placements/<int:pk>/', views.PlacementRetrieveUpdateDestroyView.as_view(), name='placement-detail'),
    path('register/', views.UserRegistrationView.as_view(), name='api-register'),
    path('login/', views.UserLoginView.as_view(), name='api-login'),
    path('current-user/', views.CurrentUserView.as_view(), name='api-current-user'),
    path('logout/', views.LogoutView.as_view(), name='api-logout'),
]
