from rest_framework import serializers
from ..models import Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    evaluator_username = serializers.CharField(source='evaluator.username', read_only=True)
    
    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ['student', 'evaluator', 'submitted_at']