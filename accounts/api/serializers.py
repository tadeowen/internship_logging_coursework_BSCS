from rest_framework import serializers
from ..models import User, InternshipProfile, InternshipPlacement, Department, Company, AcademicYear


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


class InternshipPlacementSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    supervisor_username = serializers.CharField(source='company_supervisor.username', read_only=True)
    lecturer_username = serializers.CharField(source='university_supervisor.username', read_only=True)
    student = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='code')
    academic_year = serializers.SlugRelatedField(queryset=AcademicYear.objects.all(), slug_field='name')
    company_supervisor = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', required=False, allow_null=True)
    university_supervisor = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', required=False, allow_null=True)

    class Meta:
        model = InternshipPlacement
        fields = '__all__'
        read_only_fields = []
