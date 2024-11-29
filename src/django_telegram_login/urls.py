from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('home.urls')),
    # path('account/', include('users.urls')),
]

handler404 = "django_telegram_login.views.page_not_found_view"
