import asyncio
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.conf import settings

# Переменная для отслеживания состояния бота
bot_running = False

# Функция для ответа на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на команду /start и остановка бота."""
    global bot_running  # Указываем, что будем изменять глобальную переменную bot_running

    if bot_running:
        # Бот уже запущен, останавливаем его
        await update.message.reply_text("Бот остановлен!")
        print("Бот остановлен")
        bot_running = False
        # Останавливаем бота
        await context.application.stop()
    else:
        # Бот еще не запущен, запускаем его
        bot_running = True
        await update.message.reply_text("Бот запущен!")
        print("Бот запущен")

# Функция для запуска бота в асинхронном цикле
async def run_telegram_bot():
    """Запуск бота с использованием asyncio."""
    application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    # Регистрация команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    await application.run_polling()  # Запуск бота с внутренним управлением циклом событий

# Функция для старта бота в фоновом потоке
def start_bot_in_thread():
    """Запуск бота в фоновом потоке."""
    global bot_running

    if not bot_running:
        print("Запуск бота в фоновом потоке...")

        # Создаем новый цикл событий для фонового потока
        new_loop = asyncio.new_event_loop()
        threading.current_thread().loop = new_loop  # Привязываем цикл событий к текущему потоку
        asyncio.set_event_loop(new_loop)  # Устанавливаем цикл событий в текущем потоке

        # Запуск асинхронной задачи в новом цикле событий
        new_loop.create_task(run_telegram_bot())
        new_loop.run_forever()  # Запуск цикла событий в фоновом потоке
    else:
        print("Бот уже запущен")
