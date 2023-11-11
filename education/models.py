from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='Изображение', null=True, blank=True)
    description = models.TextField(verbose_name='Описание курса', null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    preview = models.ImageField(upload_to='lesson/', verbose_name='Изображение', null=True, blank=True)
    description = models.TextField(verbose_name='Описание урока', null=True, blank=True)
    link_video = models.TextField(verbose_name='Ссылка на видео', null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
