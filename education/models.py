from django.db import models
from datetime import datetime

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


class Payment(models.Model):
    PAY_METHOD_CHOICE = (
        ('Cash', 'Наличные'),
        ('Card', 'Карта'),
    )

    date = models.DateField(auto_now_add=True, verbose_name='дата')
    price = models.IntegerField(verbose_name='Цена', null=True, blank=True)
    method = models.CharField(max_length=10, choices=PAY_METHOD_CHOICE, default='Card', verbose_name='Способ оплаты')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user} ({self.date}) - {self.price}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
