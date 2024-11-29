from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Класс UserProfile представляет профиль пользователя в системе.

    Атрибуты:
    - user: связь с моделью User, на которую ссылается профиль.
    - telegram_id: уникальный идентификатор пользователя в Telegram.
    - telegram_username: имя пользователя в Telegram.
    
    Методы:
    - __str__: возвращает имя пользователя в Telegram.
    - Meta: метаданные модели, включая человекопонятные названия и порядок сортировки.
    """
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE, 
                                related_name='profile')

    telegram_id = models.CharField(max_length=100, 
                                   unique=True, 
                                   blank=True, 
                                   null=True)

    telegram_username = models.CharField(max_length=100, 
                                         blank=True, 
                                         null=True)
    
    def __str__(self):
        return self.telegram_username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['telegram_username']