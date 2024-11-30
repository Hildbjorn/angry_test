import asyncio
import threading
import os
import signal
import sys
from django.conf import settings
from django.utils import timezone
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Путь к файлу состояния бота в папке приложения
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BOT_STATE_FILE = os.path.join(APP_DIR, 'bot_state.txt')

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я Telegram-бот.")

# Функция для завершения работы бота (удаление файла состояния)
def stop_bot():
    if os.path.exists(BOT_STATE_FILE):
        os.remove(BOT_STATE_FILE)  # Удаляем файл состояния
        print("Файл состояния бота удален.")

# Функция для запуска бота
def run_bot():
    # Если файл состояния существует, это значит, что бот уже запущен
    if os.path.exists(BOT_STATE_FILE):
        print("Бот запущен.")
        return

    # Создаем файл, чтобы отметить, что бот запущен
    with open(BOT_STATE_FILE, 'w') as f:
        f.write(f"bot_running: {timezone.now()}")  # Записываем время запуска

    try:
        # Создаем новый event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Настройка и запуск бота
        application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler("start", start))

        print("Запуск бота...")

        # Запускаем бота
        application.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

    finally:
        # После завершения работы бота удаляем файл состояния
        stop_bot()
        print("Бот завершил работу.")

# Обработчик завершения работы сервера Django
def handle_shutdown_signal(signal, frame):
    print("Завершение работы сервера Django... удаление файла состояния бота.")
    stop_bot()
    sys.exit(0)

# Регистрируем обработчик сигнала SIGINT и SIGTERM для правильной обработки завершения работы сервера
signal.signal(signal.SIGINT, handle_shutdown_signal)
signal.signal(signal.SIGTERM, handle_shutdown_signal)
