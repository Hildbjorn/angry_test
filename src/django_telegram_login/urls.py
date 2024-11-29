from django.contrib import admin
from django.urls import include, path

from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('account/', include('users.urls')),
]

handler404 = "django_telegram_login.views.page_not_found_view"
