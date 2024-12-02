from django.urls import path
from django.contrib.auth import views as auth_views

from .bot import *
from .views import *

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('start_telegram_auth/', start_telegram_auth, name='start_telegram_auth'),
    path('telegram_webhook/', telegram_webhook, name='telegram_webhook'),
    path('telegram_auth/', telegram_auth, name='telegram_auth'),
    path('check_auth/', check_auth, name='check_auth'),
]

# Дополнительный маршрут для выхода
urlpatterns += [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]