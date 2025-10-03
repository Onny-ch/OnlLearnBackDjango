from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Укажите почту",
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефон",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город проживания",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Имя пользователя",
        help_text="Укажите отправителя платежа",
    )
    payment_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата платежа",
    )
    paid_course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс или урок",
        help_text="Укажите оплаченный курс или урок",
        on_delete=models.SET_NULL,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс или урок",
        help_text="Укажите оплаченный курс или урок",
        on_delete=models.SET_NULL,
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Оплата",
        help_text="Укажите оплату",
    )
    payment_method = models.CharField(
        max_length=50,
        verbose_name="Метод оплаты",
        help_text="Укажите метод оплаты",
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"Оплата пользователя - {self.user}"
