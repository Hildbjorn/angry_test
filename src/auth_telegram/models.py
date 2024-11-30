from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Дополнительные данные для модели пользователя.
    """
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE, 
                                related_name='profile')
    
    telegram_id = models.CharField(max_length=100, 
                                   unique=True, 
                                   blank=True, 
                                   null=True, 
                                   verbose_name="Telegram ID")
    
    telegram_username = models.CharField(max_length=100, 
                                         blank=True, 
                                         null=True, 
                                         verbose_name="Telegram Username")

    def __str__(self):
        return self.telegram_username
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['telegram_username']
