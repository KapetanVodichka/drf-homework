from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    Member = 'member', _('member')
    Moderator = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', null=True, blank=True)
    phone = models.CharField(max_length=30, verbose_name='Телефон', blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name='Город', blank=True, null=True)

    role = models.CharField(max_length=9, choices=UserRole.choices, default=UserRole.Member, verbose_name='роль')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
