from django.urls import path
from .views import *

urlpatterns = [
    path('start-bot/', start_telegram_bot, name='start_bot'),
]
