import asyncio
import os
import signal
import sys
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.auth.models import User
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from .models import UserProfile

# Путь к файлу состояния бота в папке приложения
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BOT_STATE_FILE = os.path.join(APP_DIR, 'bot_state.txt')

# Синхронные операции с базой данных обернуты в sync_to_async
@sync_to_async
def get_user_by_telegram_id(telegram_id):
    """Получение пользователя по Telegram ID."""
    try:
        return User.objects.get(profile__telegram_id=telegram_id)
    except User.DoesNotExist:
        return None

@sync_to_async
def create_user_with_profile(telegram_id, telegram_username):
    """Создание пользователя и профиля."""
    user = User.objects.create_user(username=telegram_id, password=telegram_id)
    profile = UserProfile.objects.create(
        user=user, 
        telegram_id=telegram_id, 
        telegram_username=telegram_username
    )
    return user

@sync_to_async
def get_telegram_username(user):
    """Получение telegram_username пользователя из профиля."""
    return user.profile.telegram_username

# Асинхронный обработчик команды /start
async def start(update: Update, context: CallbackContext):
    user_telegram_id = str(update.message.from_user.id)
    user_telegram_username = update.message.from_user.username

    await update.message.reply_text("Проверяю наличие пользователя...")

    # Проверяем, существует ли пользователь с таким Telegram ID
    existing_user = await get_user_by_telegram_id(user_telegram_id)
    
    if existing_user:
        # Получаем telegram_username через sync_to_async
        telegram_username = await get_telegram_username(existing_user)
        await update.message.reply_text(f"Добро пожаловать обратно, {telegram_username}!")
        user = existing_user
    else:
        # Создаем нового пользователя и профиль
        user = await create_user_with_profile(user_telegram_id, user_telegram_username)
        await update.message.reply_text(f"Создан новый пользователь с ID {user.username}.")

    # В Django логиним пользователя
    # Важно: поскольку мы работаем с асинхронным контекстом, используется sync_to_async для синхронных операций
    user = await sync_to_async(login)(context.bot, user)
    
    # Получаем текущую сессию для пользователя
    session = Session.objects.get(session_key=context.bot.id)
    session_data = session.get_decoded()
    
    # Пример: можно установить дополнительные параметры сессии, если необходимо
    session_data['user_telegram_id'] = user_telegram_id
    session_data['user_telegram_username'] = user_telegram_username
    session.save()

    telegram_username = await get_telegram_username(user)
    await update.message.reply_text(f"Вы успешно аутентифицированы, {telegram_username}!")

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
    print("Завершение работы сервера Django... Остановка бота.")
    stop_bot()
    sys.exit(0)

# Регистрируем обработчик сигнала SIGINT и SIGTERM для правильной обработки завершения работы сервера
signal.signal(signal.SIGINT, handle_shutdown_signal)
signal.signal(signal.SIGTERM, handle_shutdown_signal)
