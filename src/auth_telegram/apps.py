import threading
from django.apps import AppConfig

class AuthTelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_telegram'

    def ready(self):
        from .bot import run_bot
        # Запускаем бота только при старте Django
        if not hasattr(self, 'bot_started'):  # Проверяем, был ли уже запущен бот
            self.bot_started = True
            print("Запуск бота...")

            # Запускаем бота в отдельном потоке
            threading.Thread(target=run_bot, daemon=True).start()

        else:
            print("Бот уже был запущен.")
