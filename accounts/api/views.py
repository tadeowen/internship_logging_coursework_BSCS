from rest_framework import generics, permissions, filters
from ..models import User, InternshipProfile
from .serializers import UserSerializer, InternshipProfileSerializer

try:
    from django_filters.rest_framework import DjangoFilterBackend
    FILTER_BACKENDS = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
except ImportError:
    FILTER_BACKENDS = [filters.SearchFilter, filters.OrderingFilter]

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = FILTER_BACKENDS
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']
    ordering = ['-date_joined']

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only admins can create users
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only admins can update/delete users
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class InternshipProfileListCreateView(generics.ListCreateAPIView):
    queryset = InternshipProfile.objects.all()
    serializer_class = InternshipProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = FILTER_BACKENDS
    filterset_fields = ['student__role', 'supervisor__role', 'lecturer__role']
    search_fields = ['student__username', 'company_name']
    ordering_fields = ['start_date', 'end_date']
    ordering = ['-start_date']

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only admins can create internship profiles
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class InternshipProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InternshipProfile.objects.all()
    serializer_class = InternshipProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only admins can update/delete internship profiles
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
