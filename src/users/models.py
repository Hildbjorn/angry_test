from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import ProfileManager


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Класс UserProfile представляет профиль пользователя в системе.

    Атрибуты:
    - telegram_id: уникальный идентификатор пользователя в Telegram.
    - telegram_username: имя пользователя в Telegram.

    Методы:
    - __str__: возвращает имя пользователя в Telegram.
    - Meta: метаданные модели, включая человекопонятные названия и порядок сортировки.

    """
    telegram_id = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='ID в Telegram'
    )
    telegram_username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Имя пользователя Telegram'
    )

    # Дополнительные стандартные поля
    is_active = models.BooleanField(default=False, 
                                    verbose_name='Активен')
    
    is_staff = models.BooleanField(default=False, 
                                   verbose_name='Сотрудник')
    
    date_joined = models.DateTimeField(auto_now_add=True, 
                                       verbose_name='Дата регистрации')

    USERNAME_FIELD = 'telegram_id'  # Поле для аутентификации
    REQUIRED_FIELDS = []  # Поля, которые требуют ввода при создании суперпользователя

    objects = ProfileManager()

    def __str__(self):
        return self.telegram_username or str(self.telegram_id)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['telegram_username']
