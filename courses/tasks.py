from datetime import timedelta
from dateutil.relativedelta import relativedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from courses.models import Course, Subscription
from users.models import User


@shared_task
def send_info(course_id: int) -> None:
    """Отправляет сообщение пользователю об обновлении материалов курса"""

    course = Course.objects.get(id=course_id)
    course_subscriptions = Subscription.objects.filter(course=course)
    emails_list = course_subscriptions.values_list('user__email', flat=True)
    message = f'Изменен курс {course.name}'
    send_mail(subject=f'Курс {course_id} обновлен',
              message=message,
              from_email=EMAIL_HOST_USER,
              recipient_list=emails_list)


@shared_task
def deactivate_user():
    """Деактивирует пользователей, которые не входили в систему более 30 дней."""
    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    month_ago = today - relativedelta(months=1)
    users = User.objects.filter(last_login__lte=month_ago, is_active=True)
    users.update(is_active=False)


