from rest_framework import serializers
from ..models import LogEntry

class LogEntrySerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    
    class Meta:
        model = LogEntry
        fields = '__all__'
        read_only_fields = ['student', 'created_at']