from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="courses/previews",
        null=True,
        blank=True,
        verbose_name="Превью курса",
        help_text="Загрузите превью для курса",
    )
    description = models.TextField(
        verbose_name="Описание курса",
        blank=True,
        null=True,
    )
    creator = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Имя пользователя",
        help_text="Укажите создателя курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание курса",
    )
    preview = models.ImageField(
        upload_to="courses/previews",
        null=True,
        blank=True,
        verbose_name="Превью курса",
        help_text="Загрузите превью для курса",
    )
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс для урока",
    )
    video_url = models.URLField(
        null=True,
        blank=True,
        verbose_name="Ссылка на урок",
        help_text="Добавьте ссылку формата 'https://ссылка_на_урок'",
    )
    creator = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Имя пользователя",
        help_text="Укажите создателя урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
