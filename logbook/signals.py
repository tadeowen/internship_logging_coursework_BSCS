from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LogEntry, Notification, WeeklyReport


@receiver(post_save, sender=LogEntry)
def notify_student_when_log_reviewed(sender, instance, created, **kwargs):
    if created or instance.status == 'pending':
        return
    Notification.objects.get_or_create(
        recipient=instance.student,
        title='Daily log reviewed',
        message=f'Your log for {instance.date} was {instance.status}.',
        url='/logbook/my-logs/',
    )


@receiver(post_save, sender=WeeklyReport)
def notify_student_when_weekly_report_reviewed(sender, instance, created, **kwargs):
    if created or instance.status == 'pending':
        return
    Notification.objects.get_or_create(
        recipient=instance.student,
        title='Weekly report reviewed',
        message=f'Your report for week {instance.week_start} was {instance.status}.',
        url='/logbook/weekly-reports/',
    )
