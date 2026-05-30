from rest_framework import generics, permissions, filters
from ..models import LogEntry
from .serializers import LogEntrySerializer

try:
    from django_filters.rest_framework import DjangoFilterBackend
    FILTER_BACKENDS = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
except ImportError:
    FILTER_BACKENDS = [filters.SearchFilter, filters.OrderingFilter]

class LogEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = LogEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = FILTER_BACKENDS
    filterset_fields = ['status', 'student__role']
    search_fields = ['student__username', 'activities']
    ordering_fields = ['date', 'hours_worked', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        # Users can only see their own log entries unless they are supervisors/lecturers/admin
        user = self.request.user
        if user.role == 'admin':
            return LogEntry.objects.all()
        elif user.role in ['supervisor', 'lecturer']:
            # Supervisors and lecturers can see log entries of students assigned to them
            if user.role == 'supervisor':
                return LogEntry.objects.filter(student__profile__supervisor=user)
            else:  # lecturer
                return LogEntry.objects.filter(student__profile__lecturer=user)
        else:  # student
            return LogEntry.objects.filter(student=user)

    def perform_create(self, serializer):
        # Only students can create log entries for themselves
        if self.request.user.role == 'student':
            serializer.save(student=self.request.user)
        else:
            # For other roles, they can create entries but need to specify student
            serializer.save()

class LogEntryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LogEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only access their own log entries unless they have appropriate permissions
        user = self.request.user
        if user.role == 'admin':
            return LogEntry.objects.all()
        elif user.role in ['supervisor', 'lecturer']:
            if user.role == 'supervisor':
                return LogEntry.objects.filter(student__profile__supervisor=user)
            else:  # lecturer
                return LogEntry.objects.filter(student__profile__lecturer=user)
        else:  # student
            return LogEntry.objects.filter(student=user)

    def perform_update(self, serializer):
        # Only supervisors can update log entries (for approval/comments)
        # Students can only update their own pending entries
        user = self.request.user
        log_entry = self.get_object()
        
        if user.role == 'student':
            # Students can only update their own pending entries
            if log_entry.student != user or log_entry.status != 'pending':
                self.permission_denied(self.request)
        elif user.role not in ['supervisor', 'admin']:
            # Only supervisors and admins can update others' entries
            self.permission_denied(self.request)
            
        serializer.save()

    def perform_destroy(self, instance):
        # Only admins can delete log entries
        user = self.request.user
        if user.role != 'admin':
            self.permission_denied(self.request)
        instance.delete()
