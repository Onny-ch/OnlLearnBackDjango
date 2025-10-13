from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def sending_a_course_update_email(email):
    send_mail(
        "Обновление курса2.",
        "Курс, на который вы подписаны, обновлен! Проверьте обновление.",
        settings.EMAIL_HOST_USER,
        [email],
    )
    print("All ok!")
