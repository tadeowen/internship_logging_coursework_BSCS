from rest_framework import serializers
from ..models import User, InternshipProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone']
        read_only_fields = ['id']

class InternshipProfileSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    supervisor_username = serializers.CharField(source='supervisor.username', read_only=True)
    lecturer_username = serializers.CharField(source='lecturer.username', read_only=True)
    
    class Meta:
        model = InternshipProfile
        fields = '__all__'
        read_only_fields = ['student']