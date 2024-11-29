from django.core.management.base import BaseCommand
from users.telegram_bot import start_bot

class Command(BaseCommand):
    help = 'Запускает Telegram-бота'

    def handle(self, *args, **kwargs):
        """Запуск Telegram-бота"""
        start_bot()
