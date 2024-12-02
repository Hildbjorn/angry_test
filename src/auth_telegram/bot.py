import asyncio
import os
import signal
import sys
import uuid
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, JsonResponse
from telegram import Bot, Update, User
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from .models import TelegramAuthToken

__all__ = (
    'start_telegram_auth',
    'start',
    'telegram_webhook',
    'telegram_auth',
)

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
BOT_NAME = 'django_telegram_login_test_bot'
bot = Bot(token=TELEGRAM_TOKEN)
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
# Путь к файлу состояния бота в папке приложения
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BOT_STATE_FILE = os.path.join(APP_DIR, 'bot_status.txt')


# Функция для получения сессии
def get_session():
    factory = RequestFactory()
    request = factory.get('/')  # Пустой запрос, можно указать любой URL
    middleware = SessionMiddleware()  # Применяем middleware для сессии
    middleware.process_request(request)  # Применяем сессию к запросу
    return request.session  # Возвращаем сессию

async def authenticate_user(session, token, user_data):
    """Общая логика аутентификации"""
    session_token = session.get('telegram_auth_token')
    if token == session_token:
        user, _ = User.objects.get_or_create(
            username=f'tg_{user_data["user_id"]}',
            defaults={'first_name': user_data['first_name']},
        )
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(session, user)  # Это установит сессию
        del session['telegram_auth_token']  # Удаляем токен из сессии
        return {'status': 'success'}
    return {'status': 'failure', 'message': 'Invalid token'}

def start_telegram_auth(request):
    token = str(uuid.uuid4())  # Генерация уникального токена
    TelegramAuthToken.objects.create(token=token, user_id=None)  # Создаем запись в базе
    telegram_url = f'https://t.me/{BOT_NAME}?start={token}'
    return redirect(telegram_url)

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = Update.de_json(request.body.decode('utf-8'), bot)
        application.process_update(update)
    return HttpResponse('ok')

@csrf_exempt
def telegram_auth(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            auth_token = TelegramAuthToken.objects.get(token=token)
            if auth_token.user_id:
                user, _ = User.objects.get_or_create(
                    username=f'tg_{auth_token.user_id}',
                    defaults={'first_name': request.POST.get('first_name')},
                )
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'failure', 'message': 'Токен не привязан к пользователю.'})
        except TelegramAuthToken.DoesNotExist:
            return JsonResponse({'status': 'failure', 'message': 'Недействительный токен.'})

@sync_to_async
def get_auth_token(token):
    return TelegramAuthToken.objects.get(token=token)

@sync_to_async
def save_auth_token(auth_token):
    auth_token.save()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        token = args[0]  # Токен из аргументов команды
        user_data = {
            'user_id': update.effective_user.id,
            'username': update.effective_user.username,
            'first_name': update.effective_user.first_name,
        }

        # Получаем сессию через RequestFactory
        session = get_session()  # Получаем сессию

        try:
            # Ищем токен в базе данных
            auth_token = await get_auth_token(token)

            # Если токен еще не привязан к пользователю, привязываем его
            if auth_token.user_id is None:
                auth_token.user_id = user_data['user_id']
                await save_auth_token(auth_token)

                # Вызываем функцию авторизации с передачей сессии
                result = await authenticate_user(session, token, user_data)

                if result['status'] == 'success':
                    await update.message.reply_text('Вы успешно авторизованы! Вернитесь на сайт.')
                else:
                    await update.message.reply_text('Ошибка авторизации: ' + result.get('message', 'Неизвестная ошибка'))
            else:
                await update.message.reply_text('Токен уже использован.')
        except TelegramAuthToken.DoesNotExist:
            await update.message.reply_text('Недействительный токен.')
    else:
        await update.message.reply_text('Токен отсутствует.')


application.add_handler(CommandHandler('start', start))

def stop_bot():
    """ Функция для завершения работы бота (удаление файла состояния) """
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
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
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