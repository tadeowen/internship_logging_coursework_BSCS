from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import AcademicYear, Company, Department, InternshipPlacement, StudentProfile, User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'phone']


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'registration_number',
            'department',
            'programme',
            'year_of_study',
            'emergency_contact',
            'emergency_phone',
        ]


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'contact_person', 'contact_email', 'contact_phone', 'industry', 'is_active']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['name', 'start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class InternshipPlacementForm(forms.ModelForm):
    class Meta:
        model = InternshipPlacement
        fields = [
            'student',
            'company',
            'department',
            'academic_year',
            'company_supervisor',
            'university_supervisor',
            'title',
            'start_date',
            'end_date',
            'expected_working_days',
            'status',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(role='student')
        self.fields['company_supervisor'].queryset = User.objects.filter(role='supervisor')
        self.fields['university_supervisor'].queryset = User.objects.filter(role='lecturer')
