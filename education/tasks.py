from datetime import timezone

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from education.models import Subscription
from users.models import User


@shared_task
def check_update(instance_pk, instance_title, instance_user_email, instance_user_pk):
    if Subscription.objects.filter(user=instance_user_pk, course=instance_pk):
        send_mail(
            subject='Обновление материалов курса',
            message=f'Здравствуйте!\n\nНа курсе "{instance_title}" появились новые материалы. Проверьте обновления!',
            from_email=f'{EMAIL_HOST_USER}',
            recipient_list={instance_user_email}
        )


@shared_task
def check_inactive_users():
    inactive_users = User.objects.filter(last_login__lt=timezone.now() - timezone.timedelta(days=30))

    for user in inactive_users:
        user.is_active = False
        user.save()