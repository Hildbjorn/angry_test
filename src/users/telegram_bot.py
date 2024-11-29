from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.contrib.auth import authenticate, login
from django.conf import settings
from asgiref.sync import sync_to_async
from .models import UserProfile

@sync_to_async
def get_or_create_user(telegram_id, telegram_username):
    """Обертка для асинхронного вызова get_or_create."""
    return UserProfile.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={'telegram_username': telegram_username}
    )

@sync_to_async
def save_user(user_profile):
    """Обертка для асинхронного сохранения пользователя."""
    user_profile.save()

@sync_to_async
def authenticate_user(telegram_id):
    """Обертка для аутентификации пользователя в Django."""
    return authenticate(telegram_id=telegram_id)

@sync_to_async
def login_user(request, user):
    """Обертка для логина пользователя в Django."""
    login(request, user)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start."""
    telegram_id = str(update.effective_user.id)
    telegram_username = update.effective_user.username

    # Используем синхронную обертку для получения/создания пользователя
    user_profile, created = await get_or_create_user(telegram_id, telegram_username)

    if created:
        # Если пользователь новый, активируем его
        user_profile.is_active = True
        await save_user(user_profile)  # Сохраняем пользователя асинхронно
        message = (
            f"Привет, {telegram_username or 'пользователь'}! "
            "Вы были успешно зарегистрированы и авторизованы."
        )
    else:
        message = (
            f"С возвращением, {telegram_username or 'пользователь'}! "
            "Вы успешно авторизованы."
        )

    # Асинхронная аутентификация пользователя в Django
    user = await authenticate_user(telegram_id)
    if user:
        # Авторизация в Django
        request = update.effective_message
        await login_user(request, user)  # Логируем пользователя в Django
        message += "\nВы успешно авторизованы в системе."
    else:
        message += "\nОшибка при авторизации."

    # Отправка сообщения в Telegram
    await update.message.reply_text(message)



def start_bot():
    """Запуск Telegram бота."""
    try:
        application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)

        print("Бот запущен")
        application.run_polling()

    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
