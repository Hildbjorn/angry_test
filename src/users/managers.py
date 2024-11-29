from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class ProfileManager(BaseUserManager):
    """
    Доработанная модель пользователя, в которой telegram_id является уникальным идентификатором
    для авторизации вместо имени пользователя
    """

    def create_user(self, telegram_id, telegram_username=None, password=None, **extra_fields):
        """
        Создает и возвращает обычного пользователя.
        """
        if not telegram_id:
            raise ValueError('Пользователь должен иметь telegram_id')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(telegram_id=telegram_id, telegram_username=telegram_username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, telegram_username=None, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(telegram_id, telegram_username, password, **extra_fields)
