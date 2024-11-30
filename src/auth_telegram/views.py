
import threading
from django.shortcuts import redirect
from auth_telegram.bot import bot_running, start_bot_in_thread

def start_telegram_bot(request):
    """
    Запускает бота в фоновом потоке и перенаправляет на страницу бота в Telegram.
    """
   
    threading.Thread(target=start_bot_in_thread, daemon=True).start()
    
    # Перенаправление на Telegram-страницу бота
    return redirect('https://t.me/django_telegram_login_test_bot')


