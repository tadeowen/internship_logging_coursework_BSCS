from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AcademicYear, Company, Department, InternshipPlacement, InternshipProfile, StudentProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Internship System', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Internship System', {'fields': ('role', 'phone')}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'contact_person', 'contact_phone', 'is_active')
    list_filter = ('is_active', 'industry')
    search_fields = ('name', 'contact_person', 'contact_email')


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'student', 'department', 'programme', 'year_of_study')
    list_filter = ('department', 'year_of_study')
    search_fields = ('registration_number', 'student__username', 'student__first_name', 'student__last_name')


@admin.register(InternshipPlacement)
class InternshipPlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'academic_year', 'company_supervisor', 'university_supervisor', 'status')
    list_filter = ('status', 'academic_year', 'department', 'company')
    search_fields = ('student__username', 'company__name')


@admin.register(InternshipProfile)
class InternshipProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'company_name', 'supervisor', 'lecturer', 'start_date', 'end_date')
