from django.db.models import Avg, Count, F, Sum
from accounts.models import Company, InternshipPlacement, User
from logbook.models import Attendance, LogEntry, WeeklyReport
from evaluation.models import Evaluation
from datetime import date, timedelta

class AnalyticsService:
    """Service class for handling analytics and reporting logic"""
    
    @staticmethod
    def get_internship_progress(student):
        """
        Calculate internship progress percentage for a student
        based on completed log entries vs expected duration
        """
        try:
            profile = student.profile
            total_days = (profile.end_date - profile.start_date).days
            if total_days <= 0:
                return 0
            
            # Count approved log entries
            approved_days = LogEntry.objects.filter(
                student=student,
                status='approved'
            ).aggregate(total_hours=Sum('hours_worked'))['total_hours'] or 0
            
            # Assuming 8 hours per work day
            work_days_completed = approved_days / 8
            progress_percentage = min((work_days_completed / total_days) * 100, 100)
            return round(progress_percentage, 2)
        except:
            return 0

    @staticmethod
    def get_attendance_percentage(student):
        total = Attendance.objects.filter(student=student).count()
        if total == 0:
            return 0
        present = Attendance.objects.filter(student=student, status__in=['present', 'late']).count()
        return round((present / total) * 100, 2)

    @staticmethod
    def get_student_dashboard(student):
        logs = LogEntry.objects.filter(student=student)
        total_logs = logs.count()
        approved_logs = logs.filter(status='approved').count()
        pending_logs = logs.filter(status='pending').count()
        active_placement = student.placements.filter(status='active').first()
        completion = active_placement.completion_percentage if active_placement else AnalyticsService.get_internship_progress(student)

        return {
            'total_days_logged': total_logs,
            'approved_entries': approved_logs,
            'pending_entries': pending_logs,
            'completion_percentage': completion,
            'attendance_percentage': AnalyticsService.get_attendance_percentage(student),
            'weekly_reports': WeeklyReport.objects.filter(student=student).count(),
            'active_placement': active_placement,
        }

    @staticmethod
    def get_supervisor_dashboard(supervisor):
        placements = InternshipPlacement.objects.filter(company_supervisor=supervisor)
        students = User.objects.filter(placements__in=placements).distinct()
        return {
            'students_supervised': students.count(),
            'pending_reviews': LogEntry.objects.filter(student__in=students, status='pending').count(),
            'attendance_records': Attendance.objects.filter(student__in=students).count(),
            'students': students,
        }

    @staticmethod
    def get_admin_dashboard():
        return {
            'total_students': User.objects.filter(role='student').count(),
            'total_companies': Company.objects.count(),
            'total_supervisors': User.objects.filter(role__in=['supervisor', 'lecturer']).count(),
            'active_placements': InternshipPlacement.objects.filter(status='active').count(),
            'pending_logs': LogEntry.objects.filter(status='pending').count(),
        }
    
    @staticmethod
    def get_student_ranking():
        """
        Rank students based on their average evaluation scores
        """
        students = User.objects.filter(role='student')
        rankings = []
        
        for student in students:
            avg_score = Evaluation.objects.filter(
                student=student
            ).aggregate(avg_score=Avg(
                (F('punctuality') + F('technical_skills') + F('communication') + F('initiative') + F('teamwork')) / 5
            ))['avg_score']
            
            if avg_score is None:
                avg_score = 0
                
            rankings.append({
                'student': student,
                'average_score': round(avg_score, 2),
                'total_evaluations': Evaluation.objects.filter(student=student).count()
            })
        
        # Sort by average score descending
        rankings.sort(key=lambda x: x['average_score'], reverse=True)
        return rankings
    
    @staticmethod
    def get_evaluation_trends(months=6):
        """
        Get evaluation trends over the last N months
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=30*months)
        
        trends = Evaluation.objects.filter(
            submitted_at__date__gte=start_date
        ).extra(
            select={'month': "strftime('%%Y-%%m', submitted_at)"}
        ).values('month').annotate(
            count=Count('id'),
            avg_score=Avg(
                (F('punctuality') + F('technical_skills') + F('communication') + F('initiative') + F('teamwork')) / 5
            )
        ).order_by('month')
        
        return list(trends)
    
    @staticmethod
    def get_monthly_activity(months=6):
        """
        Get monthly activity (log entries) trends
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=30*months)
        
        activity = LogEntry.objects.filter(
            date__gte=start_date
        ).extra(
            select={'month': "strftime('%%Y-%%m', date)"}
        ).values('month', 'status').annotate(
            count=Count('id')
        ).order_by('month', 'status')
        
        return list(activity)
