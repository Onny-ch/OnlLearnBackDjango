from celery import shared_task

# from django.conf import settings
# from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def check_user_by_last_login_date():
    today = timezone.now().today()
    users = User.objects.all()
    for user in users:
        if user.last_login is None:
            continue
        us_ll = (today.date() - user.last_login.date()).days
        if us_ll > 31:
            user.is_active = False
            user.save()
