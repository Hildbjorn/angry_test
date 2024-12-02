"""
Django settings for django_telegram_login project.
Generated by 'django-admin startproject' using Django 5.1.3.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
# Построение пути внутри проекта следующим образом: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Построение пути к файлу .env
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Секретный ключ
SECRET_KEY = os.environ.get('SECRET_KEY')

# Режим отладки
DEBUG = os.environ.get('DEBUG', '').lower() in ['true', '1', 'yes']

# Разрешенные хосты
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# Определение приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth_telegram',
]

# Промежуточное ПО
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной файл маршрутов
ROOT_URLCONF = 'django_telegram_login.urls'

# Папка с шаблонами
TEMPLATES_BASE_DIR = os.path.join(BASE_DIR, 'templates')

# Шаблоны Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_BASE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-приложения для проекта
WSGI_APPLICATION = 'django_telegram_login.wsgi.application'

# Конфигурация базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Движок базы данных
        'NAME': BASE_DIR / os.environ.get('DATABASE_NAME'),  # Имя базы данных
    }
}

# Проверка пароля
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Перенаправление на домашний URL после входа
LOGIN_REDIRECT_URL = '/'
# Перенаправление на домашний URL после выхода
LOGOUT_REDIRECT_URL = '/'

# Настройки интернационализации
LANGUAGE_CODE = 'ru-RU'

# Часовой пояс
TIME_ZONE = 'Europe/Moscow'

# Включение интернационализации (I18N)
USE_I18N = True

# Включение локализации (L10N)
USE_L10N = True

# Включение поддержки часовых поясов
USE_TZ = True

# Найденные статические файлы
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Дополнительные папки для статических файлов
STATICFILES_DIRS = [
    BASE_DIR.joinpath('static'),
]

# Папка для собранных статических файлов
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')

# Базовый URL для статических файлов
STATIC_URL = '/static/'

# Тип поля первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки Telegram бота, с которым будет происходить авторизация
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
