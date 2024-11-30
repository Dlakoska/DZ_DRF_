from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_info(course_id, recipients, message):
    """Отправляет сообщение пользователю об обновлении материалов курса"""

    send_mail(f'Курс {course_id} обновлен', message,
              EMAIL_HOST_USER, recipients)
    print(f'отправил {recipients}')


@shared_task
def deactivate_user():
    """Деактивирует пользователей, которые не входили в систему более 30 дней."""
    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} отключен')
        else:
            print(f'Пользователь {user.email} активен')

