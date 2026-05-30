from rest_framework import generics, permissions, filters
from ..models import Evaluation
from .serializers import EvaluationSerializer

try:
    from django_filters.rest_framework import DjangoFilterBackend
    FILTER_BACKENDS = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
except ImportError:
    FILTER_BACKENDS = [filters.SearchFilter, filters.OrderingFilter]

class EvaluationListCreateView(generics.ListCreateAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = FILTER_BACKENDS
    filterset_fields = ['student__role', 'evaluator_type', 'evaluator__role']
    search_fields = ['student__username', 'evaluator__username', 'comments']
    ordering_fields = ['submitted_at', 'punctuality', 'technical_skills', 'communication', 'initiative', 'teamwork']
    ordering = ['-submitted_at']

    def get_queryset(self):
        # Users can only see evaluations based on their role
        user = self.request.user
        if user.role == 'admin':
            return Evaluation.objects.all()
        elif user.role in ['supervisor', 'lecturer']:
            # Supervisors and lecturers can see evaluations they have given and evaluations of students assigned to them
            # For simplicity, we'll show evaluations they have given and evaluations where they are the evaluator
            return Evaluation.objects.filter(evaluator=user)
        else:  # student
            return Evaluation.objects.filter(student=user)

    def perform_create(self, serializer):
        # Only supervisors and lecturers can create evaluations
        if self.request.user.role not in ['supervisor', 'lecturer']:
            self.permission_denied(self.request)
        
        # Set the evaluator and evaluator_type based on the user
        evaluator_type = 'supervisor' if self.request.user.role == 'supervisor' else 'lecturer'
        serializer.save(evaluator=self.request.user, evaluator_type=evaluator_type)

class EvaluationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only access evaluations based on their role
        user = self.request.user
        if user.role == 'admin':
            return Evaluation.objects.all()
        elif user.role in ['supervisor', 'lecturer']:
            # Supervisors and lecturers can access evaluations they have given
            return Evaluation.objects.filter(evaluator=user)
        else:  # student
            return Evaluation.objects.filter(student=user)

    def perform_update(self, serializer):
        # Only the evaluator can update their evaluation
        if self.request.user != self.get_object().evaluator and self.request.user.role != 'admin':
            self.permission_denied(self.request)
        serializer.save()

    def perform_destroy(self, instance):
        # Only the evaluator or an admin can delete an evaluation
        if self.request.user != instance.evaluator and self.request.user.role != 'admin':
            self.permission_denied(self.request)
        instance.delete()
